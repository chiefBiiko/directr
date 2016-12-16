# Get an eye for your src files

# TODO: internalize unicode; redirect stdout to terminal or file depending on arg log

import sys, os, time, datetime, subprocess

def sd4src(dirs=[os.getcwd()], mode=['r', 'py', 'js'], log=False, walk=False, display=False, delay=10.):
    """Search directories for src files.

    Note:
        For Windows, optionally display src files with notepad.exe,
        allows log creation, and searching multiple directories.
    
    Args:
        dirs (list): absolute paths of directories to be scanned
        mode (list): specifying the types of src files to gather, allowed:
        'r', 'py', 'js', 'c', 'java', 'markup', 'markdown', 'css', 'txt',
        'misc'
        log (bool): if True, sd4src saves a .txt log file in cwd
        walk (bool): if True, recursively walk down dirs[i]
        display (bool): if True, display src files in notepad
        delay (float): if display, display period for each src file in s
        
    Returns:
        list: src files found in given directories

    Examples:
        >>> import directr as dr
        # accepting all defaults, scanning cwd
        >>> dr.sd4src()
        ['C:\\foo.R', 'C:\\bar.py']
        # searching multiple directories
        >>> dr.sd4src(dirs=[os.getcwd(), 'C:\\taskschdlr'], mode='r')
        ['C:\\foo.R', 'C:\\taskschdlr\\task.R']
        # full-blown scan using walk
        >>> dr.sd4src(dirs=['C:\\'], log=True, walk=True)
        ['C:\\foo.R', 'C:\\bar.py', 'C:\\taskschdlr\\task.R', 'C:\\z\\oo.js']
    """
    # setup
    g_src = []
    mbcs = sys.getfilesystemencoding()
    exts = {'r': ['.r', '.rmd'], 'py': ['.py'], 'js': ['.js'],
            'c': ['.c', '.cpp', '.cxx', '.h', '.hpp', '.hxx'],
            'java': ['.java', '.jar', '.jad'],
            'markup': ['.html', '.htm', '.xhtml', '.xht', '.xml'],
            'markdown': ['.md', '.markdown'], 
            'css': ['.css', '.scss', '.less'], 'txt': ['.txt'],
            'misc': ['.json', '.pickle']}
    md = tuple([v for sl in [exts[m] for m in mode] for v in sl])
    dtst = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + ' UTC'
    print('#'*79 + '\n{} -  Starting search 4 {} src files...\n'.format(dtst, mode))
    if log:
        with open(os.path.join(os.getcwd(), 'sd4src_log.txt'), 'a') as f:
            f.write('#'*79 + '\n{} - Starting search 4 {} src files...\n'.format(dtst, mode))
    # gathering src files for each dir
    if not walk:
        for d in dirs:
            files = os.listdir(d)
            d_src = [f for f in files if f.lower().endswith(md)]
            g_src.extend([os.path.join(d, fl) for fl in d_src])
            print('#'*79 + '\nDir: {}\nSrc: {}\n'.format(d, d_src))
            if log:
                with open(os.path.join(os.getcwd(), 'sd4src_log.txt'), 'a') as f:
                    f.write('#'*79 + '\nDir: {}\nSrc: {}\n'.format(d, d_src))
            # calling notepad
            if display and len(d_src) > 0:
                print('Displaying src files...\n')
                for s in d_src:
                    pr = subprocess.Popen(['C:\\Windows\\System32\\notepad.exe', os.path.join(d, s)])
                    time.sleep(delay)
                    pr.terminate()
    # walking down
    elif walk:
        try:  # walking with scandir.walk() for speed up compared 2 os.walk()
            import scandir
        except ImportError as e:
            print(e + '\npip install scandir or better http://www.lfd.uci.edu/~gohlke/pythonlibs/')
        for d in dirs:
            for rt, drs, fls in scandir.walk(d):
                if '.git' in drs:  # don't go into any .git directories
                    drs.remove('.git')
                d_src = [f for f in fls if f.lower().endswith(md)]
                g_src.extend([os.path.join(rt, fl) for fl in d_src])
                d_enc = [ds.encode(mbcs, 'replace') for ds in d_src]
                rt_enc = rt.encode(mbcs, 'replace')
                print('#'*79 + '\nDir: {}\nSrc: {}\n'.format(rt_enc, d_enc))
                if log:
                    with open(os.path.join(os.getcwd(), 'sd4src_log.txt'), 'a') as f:
                        f.write('#'*79 + '\nDir: {}\nSrc: {}\n'.format(rt_enc, d_enc))
                # calling notepad
                if display and len(d_src) > 0:
                    print('Displaying src files...\n')
                    for s in d_src:
                        pr = subprocess.Popen(['C:\\Windows\\System32\\notepad.exe', os.path.join(rt, s)])
                        time.sleep(delay)
                        pr.terminate()
    # exit --- cant show encoded strings displaying and returning unicode on exit
    #g_enc = [gs.encode(mbcs, 'replace') for gs in g_src]
    dtst = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + ' UTC'
    print('#'*79 + '\n{}  - Done.\nAll src files: {}\n'.format(dtst, g_src))
    if log:
        with open(os.path.join(os.getcwd(), 'sd4src_log.txt'), 'a') as f:
            f.write('#'*79 + '\n{} - Done.\nAll src files: {}\n'.format(dtst, g_src))
    if display and len(g_src) > 0: 
        ui = raw_input('Reopen all notepad windows now? [y/n] ')
        if 'y' in ui:
            for p in g_src:
                subprocess.Popen(['C:\\Windows\\System32\\notepad.exe', p])
    return g_src
