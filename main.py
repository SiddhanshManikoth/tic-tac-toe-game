from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager,Screen



Builder.load_string("""
<option_screen>:
    BoxLayout:
        orientation:'horizontal'
        Button:
            id:O
            text: 'O'
            font_size: 200
            color: 0,1,0,1
            on_press: root.to_game_screen(O)
            
        Button:
            id:X
            text: 'X'
            font_size: 200
            color: 1,0,0,1
            on_press: root.to_game_screen(X)

<game_screen>:
    GridLayout:   
        cols: 3 
        rows: 3
        Button:
            id: 1_1
            text:' '
            on_press: root.marked("1_1")
        Button:
            id: 2_1
            text:' '
            on_press: root.marked("2_1")
        Button:
            id: 3_1
            text:' '
            on_press: root.marked("3_1")
        Button:
            id: 1_2
            text:' '
            on_press: root.marked("1_2")    
        Button:
            id: 2_2
            text:' '
            on_press: root.marked("2_2")
        Button:
            id: 3_2
            text:' '            
            on_press: root.marked("3_2")
        Button:
            id: 1_3
            text:' '
            on_press: root.marked("1_3")
        Button:
            id: 2_3
            text:' '
            on_press: root.marked("2_3")
        Button:
            id: 3_3
            text:' '
            on_press: root.marked("3_3")
            
<result_screen>
    BoxLayout:
        orientation: 'vertical'
    
        Label: 
            id:result 
            text: ''
            font_size : root.height/12 
        Button:
            id: reset
            text:' reset'
            font_size : root.height/12 
            on_press: root.reset()       
                
""")


PLAYER_SELECTED=""
x_mark_list=[]
o_mark_list=[]
class option_screen(Screen):

    def to_game_screen(self,instance):
        global PLAYER_SELECTED
        self.manager.transition.direction="left"
        self.manager.transition.duration=0.5
        self.manager.current="game_screen"
        PLAYER_SELECTED=str(instance.text)
        print(PLAYER_SELECTED)

class game_screen(Screen):
    win=''
    den="x"
    list_switch=0
    def marked(self, coordinates):
        global PLAYER_SELECTED ,x_mark_list,o_mark_list
        players_list=[x_mark_list,o_mark_list]
        button=self.ids[coordinates]
        button.text=self.den
        button.font_size=200
        if self.den=='x':
            color = (1, 0, 0, 1)
            x_mark_list.append(coordinates)
            self.cal()
            self.den = 'o'
            self.list_switch=1

        else:
            color=(0,1,0,1)
            o_mark_list.append(coordinates)
            self.cal()
            self.den = 'x'
            self.list_switch = 0

        button.disabled_color=color
        button.disabled=True
        print(x_mark_list)
        print(o_mark_list)


    def winner_screen(self):
        result = screen_manager.get_screen(name="result_screen")
        label = result.ids['result']
        self.manager.transition.direction = "left"
        self.manager.transition.duration = 0.5
        self.manager.current = "result_screen"
        label.text = f"THE WINNER IS {(self.den).upper()}"

    def cal(self):

        result = screen_manager.get_screen(name="result_screen")
        label=result.ids['result']
        players_list = [x_mark_list, o_mark_list]
        current_player_list=players_list[self.list_switch]
        if '1_1' in current_player_list:
            if '2_1' in current_player_list:
                if '3_1' in current_player_list:
                    self.winner_screen()
            if '1_2' in current_player_list:
                if '1_3' in current_player_list:
                   self.winner_screen()
            if '2_2' in current_player_list:
                if '3_3' in current_player_list:
                    self.winner_screen()
        if '3_1' in current_player_list:
            if '3_2' in current_player_list:
                if '3_3' in current_player_list:
                    self.winner_screen()
            if '2_2' in current_player_list:
                if '1_3' in current_player_list:
                    self.winner_screen()
        if '1_2' in current_player_list:
            if '2_2' in current_player_list:
                if '3_2' in current_player_list:
                    self.winner_screen()
        if '2_3' in current_player_list:
            if '2_2' in current_player_list:
                if '2_1' in current_player_list:
                    self.winner_screen()
            if '1_3' in current_player_list:
                if '3_3' in current_player_list:
                    self.winner_screen()









class result_screen(Screen):
    def __init__(self,**kwargs):
        game=screen_manager.get_screen(name="game_screen")
        super(result_screen, self).__init__(**kwargs)
        label=self.ids['result']
        label.text=f"The Winner Is {game.win}!!!"
        print(type(game.win))
    def reset(self):
        global PLAYER_SELECTED,x_mark_list,o_mark_list,win,screen_manager
        PLAYER_SELECTED = ""

        game=screen_manager.get_screen(name="game_screen")
        btn=game.ids['1_1']
        btn.disabled=False
        for btn in x_mark_list:
                btn=game.ids[btn]
                btn.text = ""
                btn.disabled=False
        for btn in o_mark_list:
                btn=game.ids[btn]
                btn.text=""
                btn.disabled=False
        x_mark_list = []
        o_mark_list = []
        game.win = ''
        game.den="x"


        self.manager.transition.direction = "right"
        self.manager.transition.duration = 0.5
        self.manager.current = "option_screen"




screen_manager=ScreenManager()


screen_manager.add_widget(option_screen(name="option_screen"))
screen_manager.add_widget(game_screen(name="game_screen"))
screen_manager.add_widget(result_screen(name="result_screen"))
class tic_tac_toe(App):
    def build(self):
        return screen_manager

if __name__ == '__main__':
    tic_tac_toe().run()