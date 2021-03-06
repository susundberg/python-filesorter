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


def make_a_file( path, sub1, fns, dt, content=None ):
  for fn in fns:
    full_path = os.path.join( path, sub1 )
    full_fn   = os.path.join( full_path, fn )
    if not os.path.exists( full_path ):
       os.makedirs( full_path )
       
    if content==None:
       content = full_fn + "\n"
       
    fid = open( full_fn, 'wb' )
    fid.write( bytearray( content, 'utf8') )
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
      self.source_dir = tempfile.mkdtemp()
      self.target_dir = tempfile.mkdtemp()
      

    def test_simple(self):
      make_a_file( self.source_dir, "sub1", ("FOO","BAR") , datetime.date( 2010,10,30) )
      make_a_file( self.source_dir, "sub2", ("FOO","BAR"), datetime.date( 2010,11,30) )
      check_files( self.source_dir, ("sub1/FOO",) )
      check_files( self.source_dir, ("sub2/FOO",) )
      sorter.main( get_me_settings( self.source_dir,  self.target_dir , "--dry_run" ) )
      check_files( self.source_dir, ("sub1/FOO",) )
      check_files( self.target_dir, ("2010-10/",), exists=False )
      sorter.main( get_me_settings( self.source_dir,  self.target_dir ) )
      check_files( self.target_dir, ("2010-10/FOO", "2010-10/BAR", "2010-11/FOO", "2010-11/BAR" ) )

    def test_rmdir(self):
      for sub in ("sub1", "sub2" ):
         make_a_file( self.source_dir, sub, ("FOO","BAR.JPEG"), datetime.date( 2010,10,30) )
      sorter.main( get_me_settings( os.path.join( self.source_dir, "sub1" ) ,  self.target_dir,  ) )
      check_files( self.source_dir, ("sub1/",), exists=True)
      sorter.main( get_me_settings( os.path.join( self.source_dir, "sub2" ) ,  self.target_dir, "--rmdir" ) )
      check_files( self.source_dir, ("sub2/",), exists=False)
            
    def test_duplicate(self):
      for sub in ("sub1", "sub2", "sub3" ):
         make_a_file( self.source_dir, sub, ("FOO","BAR.JPEG"), datetime.date( 2010,10,30) )
      sorter.main( get_me_settings( self.source_dir,  self.target_dir , "--verbose" ) )
      
    def test_duplicate_same_content( self ):
      for sub in ("sub1", "sub2", "sub3" ):
         make_a_file( self.source_dir, sub, ("FOO",), datetime.date( 2010,10,30), content="SAME CONTENT" )
      sorter.main( get_me_settings( self.source_dir,  self.target_dir , "--verbose" ) ) 
      
    def tearDown(self):
      shutil.rmtree(self.source_dir)
      shutil.rmtree(self.target_dir)
      

if __name__ == '__main__':
    unittest.main()
