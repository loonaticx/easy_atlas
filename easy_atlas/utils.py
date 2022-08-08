import ConfigParser, os

class INIHandler:
    '''INIHandler simplifies the load/save information on INI style files.'''
    
    @staticmethod
    def load_info(_file, option, debug=False):
        '''Load info from config file.
        
        Args:
            _file: short filename
            option: field where the information will be read from
            debug: boolean for printing debug information in the script editor
        '''
        
        configFilename = _file.replace("\\\\", "/")
        
        config = ConfigParser.RawConfigParser()
        config.read(configFilename)
        info = ""
        try:
            info = config.get("ROOT", option)
        except:
            pass
            
        if debug: print configFilename    
        
        return info
    
    @staticmethod
    def save_info(_file, option, info, debug=False):
        '''Save info into config file.
        
        Args:
            _file: short filename
            option: field where the information will be saved
            info: information that will be stored
            debug: boolean for printing debug information in the script editor
        '''
        
        configFilename = os.path.abspath(_file)
        configDirectory = os.path.dirname(configFilename)
        
        config = ConfigParser.RawConfigParser()
        config.read(configFilename)
        try:
            config.add_section('ROOT')
        except:
            pass
        config.set('ROOT', option, info)

        if not os.path.exists(configDirectory):
            os.makedirs(configDirectory)

        with open(configFilename, 'w+b') as configfile:
            config.write(configfile)

        if debug: print configFilename