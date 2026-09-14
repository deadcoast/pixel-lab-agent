import json,runpy,sys
sys.path[:0] = ['C:\\Users\\ryanf\\github\\pixel-lab-docsuite\\.venv\\Lib\\site-packages']
runner = 'C:\\Users\\ryanf\\github\\pixel-lab-docsuite\\evidence\\family-delivery\\plugin-scenario\\copied-kit\\scripts\\pixl.py'
sys.argv[0] = runner
runpy.run_path(runner, run_name='__main__')
