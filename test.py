import unittest
import os
import sorter
import collections
import tempfile
import shutil
import datetime
import time

def get_me_settings(*pargs):
   parser = sorter.get_parser()
   return parser.parse_args( pargs )


def make_a_file( path, sub1, fns, dt ):
  for fn in fns:
    full_path = os.path.join( path, sub1 )
    full_fn   = os.path.join( full_path, fn )
    if not os.path.exists( full_path ):
       os.makedirs( full_path )
    fid = open( full_fn, 'wb' )
    fid.write( bytearray( full_fn + "\n", 'utf8') )
    fid.close()
    mt = time.mktime( dt.timetuple() )
    os.utime( full_fn, ( mt, mt ) ) 
    
def check_files( path, files, exists=True ):
  for file in files:
    full_path = os.path.join( path, file )
    was = os.path.exists( full_path )
    if was != exists:
      raise Exception("File %s invalid exists status: %d" % (full_path, was) )

   
  
class TestSorter(unittest.TestCase):

    def setUp(self):
      self.test_dir = tempfile.mkdtemp()
      self.target_dir = tempfile.mkdtemp()
      

    def test_simple(self):
      make_a_file( self.test_dir, "sub1", ("FOO","BAR") , datetime.date( 2010,10,30) )
      make_a_file( self.test_dir, "sub2", ("FOO","BAR"), datetime.date( 2010,11,30) )
      check_files( self.test_dir, ("sub1/FOO",) )
      check_files( self.test_dir, ("sub2/FOO",) )
      sorter.main( get_me_settings( self.test_dir,  self.target_dir , "--dry_run" ) )
      check_files( self.test_dir, ("sub1/FOO",) )
      check_files( self.target_dir, ("2010-10/",), exists=False )
      sorter.main( get_me_settings( self.test_dir,  self.target_dir ) )
      check_files( self.target_dir, ("2010-10/FOO", "2010-10/BAR", "2010-11/FOO", "2010-11/BAR" ) )
      
    def test_duplicate(self):
      for sub in ("sub1", "sub2", "sub3" ):
         make_a_file( self.test_dir, sub, ("FOO","BAR.JPEG"), datetime.date( 2010,10,30) )
      sorter.main( get_me_settings( self.test_dir,  self.target_dir , "--verbose" ) )

      
    def tearDown(self):
      shutil.rmtree(self.test_dir)
      shutil.rmtree(self.target_dir)
      

if __name__ == '__main__':
    unittest.main()
