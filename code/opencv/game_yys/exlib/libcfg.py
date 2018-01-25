import ConfigParser
import re




def cleancfg(fname):
    content = open(fname).read() 
    content = re.sub(r"\xfe\xff","", content)  
    content = re.sub(r"\xff\xfe","", content)  
    content = re.sub(r"\xef\xbb\xbf","", content)  
    open(fname, 'w').write(content)


def loadcfg(cfgfile,sec,cfgnames):
    cleancfg(cfgfile)
    config = ConfigParser.RawConfigParser()
    config.read([cfgfile])
    
    result={}

    for c in cfgnames:
		result[c]=config.get(sec,c)

    return result
