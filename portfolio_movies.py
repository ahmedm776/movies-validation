"""Post-coursework portfolio improvement. Original notebook is preserved unchanged."""
import argparse,json,re,hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import pandera.pandas as pa
from cerberus import Validator
from sklearn.preprocessing import StandardScaler
import great_expectations as gx

ALLOWED={'Animation','Romance','Action','Adventure','Drama','Horror','Thriller','Crime','Mystery','Comedy'}
FILTER={'Animation','Action','Adventure','Drama','Mystery','Comedy'}
def genres(value):
    return [v.strip() for v in str(value).split(',') if v.strip()] if pd.notna(value) else []
def year_start(value):
    match=re.search(r'(?<!\d)(\d{4})(?!\d)',str(value))
    return float(match.group(1)) if match else np.nan

def run(input_path,output_dir,profile=False,pedagogical=False):
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    raw=pd.read_csv(input_path);raw.columns=raw.columns.str.strip()
    required={'MOVIES','YEAR','GENRE','RATING','VOTES','RunTime','Gross'}
    if not required.issubset(raw.columns):raise ValueError(f'Missing columns: {required-set(raw.columns)}')
    raw.to_csv(out/'input_snapshot.csv',index=False)
    # Schema inference describes observed data; it is not evidence that business rules pass.
    (out/'inferred_schema.txt').write_text(str(pa.infer_schema(raw)))
    # Real GX validation and persisted suite/checkpoint, against raw data before repair.
    context=gx.get_context(mode='ephemeral')
    ds=context.sources.add_pandas('movies')
    asset=ds.add_dataframe_asset(name='raw_movies')
    request=asset.build_batch_request(dataframe=raw)
    context.add_or_update_expectation_suite('movies_rules')
    validator=context.get_validator(batch_request=request,expectation_suite_name='movies_rules')
    for col in raw:validator.expect_column_values_to_not_be_null(col)
    validator.expect_column_values_to_be_between('RATING',min_value=1,max_value=10)
    validator.expect_column_values_to_be_unique('MOVIES')
    # Full-string token validation, not substring regex: every comma-separated genre must be allowed.
    pattern=r'^\s*(?:'+ '|'.join(sorted(ALLOWED)) +r')(?:\s*,\s*(?:'+'|'.join(sorted(ALLOWED))+r'))*\s*$'
    validator.expect_column_values_to_match_regex('GENRE',pattern)
    validator.save_expectation_suite(discard_failed_expectations=False)
    checkpoint=context.add_or_update_checkpoint(name='movies_checkpoint',validations=[{'batch_request':request,'expectation_suite_name':'movies_rules'}])
    result=checkpoint.run()
    (out/'expectation_suite.json').write_text(json.dumps(validator.get_expectation_suite(discard_failed_expectations=False).to_json_dict(),indent=2,default=str))
    (out/'checkpoint_result.json').write_text(json.dumps(result.to_json_dict(),indent=2,default=str))
    # Actual Cerberus use with token-level allowed membership and strictly greater than9.
    # Cerberus contains a list means ALL elements; use an anyof rule for the task's ANY genre condition.
    cv=Validator({'rating':{'type':'float','check_with':lambda field,value,error: error(field,'must be greater than9') if value<=9 else None},'genres':{'type':'list','anyof':[{'contains':g} for g in sorted(FILTER)]}})
    selected=[]
    for i,row in raw.iterrows():
        rating=pd.to_numeric(row['RATING'],errors='coerce')
        if pd.notna(rating) and cv.validate({'rating':float(rating),'genres':genres(row['GENRE'])}):selected.append(i)
    raw.loc[selected].to_csv(out/'rating_above9_selected_genres.csv',index=False)
    df=raw.copy()
    # Preserve original year/range; start year is explicit derived feature, never silently discard ranges.
    df['YEAR_RAW']=df['YEAR'];df['YEAR']=df['YEAR'].map(year_start)
    df['VOTES']=pd.to_numeric(df['VOTES'].astype('string').str.replace(',','',regex=False),errors='coerce').astype('float64')
    df=df.drop(columns=['Gross'])
    missing_genre=df['GENRE'].isna()|df['GENRE'].astype('string').str.strip().eq('')
    df.loc[missing_genre].to_csv(out/'missing_genre_rows.csv',index=False)
    df=df.loc[~missing_genre].copy()
    # Conservative default preserves missing years and statistical extremes.
    duplicates=int(df.duplicated().sum());df=df.drop_duplicates().copy()
    num_cols=df.select_dtypes(include='number').columns.tolist()
    q1=df[num_cols].quantile(.25);q3=df[num_cols].quantile(.75);iqr=q3-q1
    mask=((df[num_cols]<(q1-1.5*iqr))|(df[num_cols]>(q3+1.5*iqr))).any(axis=1)
    df['IQR_FLAG']=mask
    df.to_csv(out/'cleaned_preserving_missingness.csv',index=False)
    report={'input_sha256':hashlib.sha256(Path(input_path).read_bytes()).hexdigest(),'input_rows':len(raw),'gx_success':bool(result.success),'cerberus_filtered_rows':len(selected),'missing_genre_excluded':int(missing_genre.sum()),'duplicates_removed':duplicates,'iqr_flagged_not_removed':int(mask.sum()),'output_rows':len(df),'year_parsed_before_imputation':int(raw['YEAR'].map(year_start).notna().sum()),'year_missing_final':int(df['YEAR'].isna().sum()),'default_policy':'No imputation or IQR exclusion. YEAR_RAW and missingness preserved. Missing genre exclusions and exact duplicate removal are sequential; raw input snapshot preserved.'}
    if pedagogical:
        # Explicit optional assignment-style branch, never the default data product.
        teaching=df.drop(columns=['IQR_FLAG']).copy()
        for col in num_cols:
            teaching[col]=teaching[col].fillna(teaching[col].median())
        for col in teaching.select_dtypes(exclude='number'):
            if col=='YEAR_RAW':continue
            mode=teaching[col].mode(dropna=True)
            if not mode.empty:teaching[col]=teaching[col].fillna(mode.iloc[0])
        tq1=teaching[num_cols].quantile(.25);tq3=teaching[num_cols].quantile(.75);tiqr=tq3-tq1
        excluded=((teaching[num_cols]<(tq1-1.5*tiqr))|(teaching[num_cols]>(tq3+1.5*tiqr))).any(axis=1)
        teaching.loc[excluded].to_csv(out/'PEDAGOGICAL_iqr_excluded.csv',index=False)
        teaching=teaching.loc[~excluded].copy();teaching.to_csv(out/'PEDAGOGICAL_imputed_unscaled.csv',index=False)
        scaler=StandardScaler();teaching[num_cols]=scaler.fit_transform(teaching[num_cols]);teaching.to_csv(out/'PEDAGOGICAL_scaled.csv',index=False)
        report['optional_pedagogical']={'iqr_excluded':int(excluded.sum()),'rows':len(teaching),'warning':'Imputed year is not recovered release information; statistical extremes are not proven errors.'}
    (out/'run_report.json').write_text(json.dumps(report,indent=2))
    if profile:
        from ydata_profiling import ProfileReport
        ProfileReport(raw,title='Movies dataset - raw input',minimal=True).to_file(out/'movies_report.html')
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--output',default='outputs');p.add_argument('--profile',action='store_true');p.add_argument('--pedagogical',action='store_true');a=p.parse_args();print(json.dumps(run(a.input,a.output,a.profile,a.pedagogical),indent=2))
