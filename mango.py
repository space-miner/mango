import utils
import mangasee


class Option:
    def __init__(self, description, action):
        self.description = description
        self.action = action

    def __str__(self):
        return self.description


def print_options(options):
    for choice, option in options.items():
        print(f'{choice}: {option}')


def option_is_valid(choice, options):
    return choice or choice.upper() in options.keys()


def get_option(options):
    choice = input('Choose an action: ')
    while not option_is_valid(choice, options):
        print('Invalid action')
        choice = input('Choose an action: ')
    return options[choice.upper()]


def print_logo():
    print('''      __  __
     |  \/  |
     | \  / | __ _ _ __   __ _  ___
     | |\/| |/ _` | '_ \ / _` |/ _ \\
     | |  | | (_| | | | | (_| | (_) |
     |_|  |_|\__,_|_| |_|\__, |\___/
                          __/ |
                         |___/
                                                       
                              ,&#%                     
                           #(((*(##%#((/((*  %./%*.*   
                       /%/(((*((((((#%///###,(&%,/     
                    #/(((((#((((#%&&%&%&%&&&&(.,       
             (#///////((((((#%%%&%%%%%&%%%%%,..#       
                 %.,#%&&%%##(###*((//#######%%*.%      
              %,,#####(((((//,,,...  . *(/###%%#,#     
            ..,####/(/////**,,,...... ,,***((#%##.%    
           #.(#/(#//////**/*,,,,...,*********(%%%*..%  
          %/#**////////////////**********////#%(//.*#  
         (#/*////////////////////////////////%%#%/,%   
       %.#*//////////////////////////////////#%#(( .%  
      %.#//////////////////////////////////*(%#(#.#    
    (.////////////////////////////////////*#%#*/./     
(/.(#///***//////////////////////////////((((*,./      
.#////////****/////////////////////(////((%*/./,       
*///////////*******/////////////////((#%%*(..%         
(,((//////////****/***////////(((((#%%%((,.%           
  *.#%##(//////////////((((((((#%#&%%(/./#             
    %,,(%%%((#/////(//(((%(#&%&&%&%/.%                 
        (..,*(###%%%%%%%%((*,,./&#                     
              .%%&%&                                   

    ''')


def loop(options):
    utils.clear_screen()
    print_logo()
    print_options(options)
    option = get_option(options)
    option.action()


if __name__ == '__main__':
    ms = mangasee.MangaSee()
    options = {
            'U': Option('update mangasee database', ms.create_database),
            'S': Option('search for a series', ms.search),
            'D': Option('download a series', ms.download),
            'X': Option('exit', ms.exit)}
    while True:
        loop(options)
