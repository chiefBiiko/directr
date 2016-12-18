# Get an eye for your src files with py2.7
import sys, os, time, datetime, subprocess

def sd4src(dirs=[os.getcwd()], mode=['r', 'py', 'js'], log=False, walk=False, display=False, delay=10.):
    """
    Search directories for src files.

    Note:
        For Windows, optionally display src files with notepad.exe,
        allows log creation, and searching multiple directories.
    
    Args:
        dirs (list): absolute paths of directories to be scanned
        mode (list): specifying the types of src files to gather, allowed:
        'r', 'py', 'js', 'c', 'java', 'markup', 'markdown', 'css', 'txt',
        'log', 'json'
        log (bool): if True, sd4src saves a log file in cwd
        walk (bool): if True, recursively walk down dirs[i]
        display (bool): if True, display src files in notepad
        delay (float): if display, display period for each src file in s
        
    Returns:
        list: src files found in given directories

    TODO:
        Testing with non-ascii chars..
        
    Examples:
        >>> import directr as dr
        # accepting all defaults, scanning cwd
        >>> dr.sd4src()
        ['C:\\foo.R', 'C:\\bar.py']
        # searching multiple directories
        >>> dr.sd4src(dirs=[os.getcwd(), 'C:\taskschdlr'], mode=['r'])
        ['C:\\foo.R', 'C:\\taskschdlr\\task.R']
        # full-blown scan using walk
        >>> dr.sd4src(dirs=['C:\'], log=True, walk=True)
        ['C:\\foo.R', 'C:\\bar.py', 'C:\\taskschdlr\\task.R', 'C:\\z\\oo.js']
    """
    # setup
    g_log = []
    g_src = []
    ncod = sys.stdout.encoding
    notepad = 'C:\\Windows\\System32\\notepad.exe'
    exts = {'r': ['.r', '.rmd'], 'py': ['.py'], 'js': ['.js'],
            'c': ['.c', '.cpp', '.cxx', '.h', '.hpp', '.hxx'],
            'java': ['.java', '.jar', '.jad'],
            'markup': ['.html', '.htm', '.xhtml', '.xht', '.xml'],
            'markdown': ['.md', '.markdown'], 
            'css': ['.css', '.scss', '.less'], 'txt': ['.txt'],
            'log': ['.log'], 'json': ['.json']}
    md = tuple([v for sl in [exts[m] for m in mode] for v in sl])
    dtst = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + ' UTC'
    print('#'*79 + '\n{} -  Starting search 4 {} src files...\n'.format(dtst, mode))
    if log:
        with open(os.path.join(os.getcwd(), 'sd4src.log'), 'a') as f:
            f.write('#'*79 + '\n{} - Starting search 4 {} src files...\n'.format(dtst, mode))
    # gathering src files for each dir
    if not walk:
        for d in dirs:
            files = os.listdir(d)
            d_src = [f for f in files if f.lower().endswith(md)]
            g_src.extend([os.path.join(d, fl) for fl in d_src])
            g_log.append('Dir: {}\nSrc: {}\n'.format(d, ', '.join(d_src)))
            # calling notepad
            if display and len(d_src) > 0:
                print('Displaying src files...\n')
                for s in d_src:
                    pr = subprocess.Popen([notepad, os.path.join(d, s)])
                    time.sleep(delay)
                    pr.terminate()
    # walking down
    elif walk:
        try:  # walking with scandir.walk() for speed up compared 2 os.walk()
            import scandir
        except ImportError as e:
            print(e + '\npip install scandir or even better from http://www.lfd.uci.edu/~gohlke/pythonlibs/')
        for d in dirs:
            for rt, drs, fls in scandir.walk(d):  # returns unicodes
                if u'.git' in drs:  # don't go into any .git directories
                    drs.remove(u'.git')
                b_rt = rt.encode(ncod, 'replace')  # converting unicodes back 2 bytes
                d_src = [f.encode(ncod, 'replace') for f in fls if f.lower().endswith(md)]
                g_src.extend([os.path.join(b_rt, b_fl) for b_fl in d_src])
                g_log.append('Dir: {}\nSrc: {}\n'.format(b_rt, ', '.join(d_src)))
                # calling notepad
                if display and len(d_src) > 0:
                    print('Displaying src files...\n')
                    for s in d_src:
                        pr = subprocess.Popen([notepad, os.path.join(b_rt, s)])
                        time.sleep(delay)
                        pr.terminate()
    # exit
    dtst = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + ' UTC'
    g_log.append('#'*79 + '\n{} - Done.\nAll src files: {}\n'.format(dtst, ', '.join(g_src)))
    print(''.join(g_log))
    if log:
        with open(os.path.join(os.getcwd(), 'sd4src.log'), 'a') as f:
            f.write(''.join(g_log))
    if display and len(g_src) > 0: 
        ui = raw_input('Reopen all notepad windows now? [y/n] ')
        if 'y' in ui:
            for p in g_src:
                subprocess.Popen([notepad, p])
    return g_src
