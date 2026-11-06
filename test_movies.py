import json,unittest
import pandas as pd
from portfolio_movies import year_start,genres,FILTER
from cerberus import Validator
class Tests(unittest.TestCase):
 def test_year_ranges(self):
  self.assertEqual(year_start('(2010–2022)'),2010)
  self.assertEqual(year_start('(2021– )'),2021)
 def test_tokens(self):
  self.assertEqual(genres('\nAction, Drama '),['Action','Drama'])
  self.assertNotIn('Action',genres('Live Action'))
 def test_cerberus_any(self):
  v=Validator({'rating':{'type':'float','check_with':lambda field,value,error: error(field,'must be greater than9') if value<=9 else None},'genres':{'type':'list','anyof':[{'contains':g} for g in sorted(FILTER)]}})
  self.assertTrue(v.validate({'rating':9.2,'genres':['Drama','Horror']}))
  self.assertTrue(v.validate({'rating':9.0000000001,'genres':['Drama']}))
  self.assertFalse(v.validate({'rating':9.0,'genres':['Drama']}))
  self.assertFalse(v.validate({'rating':9.2,'genres':['Live Action']}))
 def test_conservation(self):
  r=json.load(open('final-output/run_report.json'))
  self.assertEqual(r['input_rows'],sum(r[k] for k in ['missing_genre_excluded','duplicates_removed','output_rows']))
  df=pd.read_csv('final-output/cleaned_preserving_missingness.csv');self.assertEqual(int(df['YEAR'].isna().sum()),579);self.assertEqual(len(df),9490)
  self.assertFalse(r['gx_success'])
  self.assertEqual(len(pd.read_csv('final-output/rating_above9_selected_genres.csv')),136)
if __name__=='__main__':unittest.main()
