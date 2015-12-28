# some generic helper functions for NetworkWrangler
import copy, xlrd

def openFileOrString(f):
    # check if it's a filename or a file. Open it if it's a filename
    if isinstance(f, str):
        f = open(f, 'w')
    elif isinstance(f, file):
        if f.closed: f = open(f.name)
    return f

def generate_unique_id(seq):
    """
    Generator that yields a number from a passed in sequence
    """
    for x in seq:
        yield x

def reproject_to_wgs84(longitude, latitude, EPSG = "+init=EPSG:2926", conversion = 0.3048006096012192):
    '''
    Converts the passed in coordinates from their native projection (default is state plane WA North-EPSG:2926)
    to wgs84. Returns a two item tuple containing the longitude (x) and latitude (y) in wgs84. Coordinates
    must be in meters hence the default conversion factor- PSRC's are in state plane feet.  
    '''
    import pyproj
    # Remember long is x and lat is y!
    prj_wgs = pyproj.Proj(init='epsg:4326')
    prj_sp = pyproj.Proj(EPSG)
    
    # Need to convert feet to meters:
    longitude = longitude * conversion
    latitude = latitude * conversion
    x, y = pyproj.transform(prj_sp, prj_wgs, longitude, latitude)
    
    return x, y

def getListOverlap(list1, list2):
    '''
    Assumes list1 and list2 are lists of integers where elements are unique within
    each list. Returns left (elements only in list1), right (elements only in list2),
    overlap (elements in both lists)
    '''
    left = removeDuplicatesFromList(list1)
    right = removeDuplicatesFromList(list2)
    overlap = []
    for x in left:
        if x in right:
            if x not in overlap: overlap.append(x)
            right.remove(x)
    for x in overlap:
        left.remove(x)
    left.sort(), right.sort(), overlap.sort()
    return (left, right, overlap)

def boilDown(numbers, left_split, right_split):
    sets = []
    overlap1 = getListOverlap(numbers, left_split)
    overlap2 = getListOverlap(numbers, right_split)
    for x in overlap1:
        if x not in sets and len(x) > 0: sets.append(x)
    for x in overlap2:
        if x not in sets and len(x) > 0: sets.append(x)
    return sets

def isSubset(subset, fullset):
    for i in subset:
        if i not in fullset:
            return False
    return True
def removeDuplicatesFromList(l):
    this_list = copy.deepcopy(l)
    for x in this_list:
        while this_list.count(x) > 1:
            this_list.remove(x)
    return this_list

def minutesPastMidnightToHHMMSS(minutes):
    if isinstance(minutes, float):
        seconds = minutes - int(minutes)
        seconds *= 60
        ss = '%02d' % int(round(seconds,0))
    else:
        ss = '00'
        
    minutes = int(minutes)
    hh = '%02d' % (minutes/60)
    mm = '%02d' % (minutes%60)
    return hh+mm+ss

def secondsPastMidnightToHHMMSS(seconds):
    seconds = int(seconds)
    hh = '%02d' % (seconds/3600)
    mm = '%02d' % ((seconds%3600)/60)
    ss = '%02d' % ((seconds%3600)%60)
    return hh+mm+ss

def getChampNodeNameDictFromFile(filename):
    book = xlrd.open_workbook(filename)
    sh = book.sheet_by_index(0)
    nodeNames = {}
    for rx in range(0,sh.nrows): # skip header
        therow = sh.row(rx)
        nodeNames[int(therow[0].value)] = therow[1].value
    return nodeNames
