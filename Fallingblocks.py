import pygame
import random
import sys

#size
WIDTH=800
HEIGHT=800
GRID=30

FPS=60
#color
LIGHT_BLUE=(0,255,255)
YELLOW=(255,255,0)
PURPLE=(139,0,139)
BLUE=(0,0,255)
ORANGE=(255,165,0)
GREEN=(0,128,0)
RED=(220,20,60)
BLACK=(0,0,0)
WHITE=(220,220,220)
GRAY=(105,105,105)

class Blocks:
    def __init__(self):
        self.I = [
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
        ]
        self.J = [
            [0, 0, 2, 0],
            [0, 0, 2, 0],
            [0, 2, 2, 0],
            [0, 0, 0, 0]
        ]
        self.L = [
            [0, 3, 0, 0],
            [0, 3, 0, 0],
            [0, 3, 3, 0],
            [0, 0, 0, 0]
        ]
        self.O = [
            [0, 0, 0, 0],
            [0, 4, 4, 0],
            [0, 4, 4, 0],
            [0, 0, 0, 0]
        ]
        self.S = [
            [0, 5, 0, 0],
            [0, 5, 5, 0],
            [0, 0, 5, 0],
            [0, 0, 0, 0]
        ]
        self.T = [
            [0, 6, 0, 0],
            [0, 6, 6, 0],
            [0, 6, 0, 0],
            [0, 0, 0, 0]
        ]
        self.Z = [
            [0, 0, 7, 0],
            [0, 7, 7, 0],
            [0, 7, 0, 0],
            [0, 0, 0, 0]
        ]
        self.color_dict={1:LIGHT_BLUE,2:BLUE,3:ORANGE,4:YELLOW,5:GREEN,6:PURPLE,7:RED}

    def get_block(self, name):
        return getattr(self, name, None)
    
    def get_block_color(self,num):
        return self.color_dict[num]

class Board:
    def __init__(self):
        #左右と下部の壁に-1を配置したボードを作成
        self.board=[]
        for i in range(21):
            row=[]
            for j in range(12):
                if i==20 or j==0 or j==11:
                    row.append(-1)
                else:
                    row.append(0)
            self.board.append(row)

class GameSystem:
    def __init__(self):
        self.generate_block()

    def generate_block(self):
        gen_flag=True
        #稼働中のブロックがある場合はgenerate flagをFalseに
        for i in range(19, -1, -1):
            for j in range(1, 11):
                if player_board.board[i][j]>0 :
                    gen_flag=False
        if gen_flag:            
            #ブロックを生成
            list=["I","J","L","O","S","T","Z"]
            next_block_matrix=blocks.get_block(random.choice(list))
            #next_block_matrix=blocks.get_block("O")
            for i in range(4):
                for j in range(4):
                    if next_block_matrix[i][j]!=0:
                        player_board.board[1+i][4+j]=next_block_matrix[i][j]

    def falling_block(self):
        block_pos_list=[]
        stop_flag=False
        color_num=0
        #落下を終了するか判定
        for i in range(19, -1, -1):
            for j in range(1, 11):
                if player_board.board[i][j]>0 :
                    block_pos_list.append((i,j))
                    color_num=player_board.board[i][j]
                    if player_board.board[i+1][j]==-1:
                        stop_flag=True
        if not stop_flag:
            #落下
            for i,j in block_pos_list:
                player_board.board[i+1][j]=player_board.board[i][j]
                player_board.board[i][j]=0
        else:
            #落下終了時にfixed boardにはカラーブロック, player boardには-1の壁ブロックを配置
            for i,j in block_pos_list:
                fixed_board.board[i][j]=color_num
                player_board.board[i][j]=-1
    
    def falling_speed_manage(self,current_time):
        global start_time
        global fall_time_interval
        global FALL
        global fall_add_flag
        elapsed_time = (current_time - start_time) / 1000.0

        #20秒経過ごとに加速
        if elapsed_time>20 and fall_add_flag==0 :
            fall_add_flag=1
            fall_time_interval /=2
            pygame.time.set_timer(FALL, int(fall_time_interval))
        elif elapsed_time>40 and fall_add_flag==1:
            fall_add_flag=2
            fall_time_interval /=2 
            pygame.time.set_timer(FALL, int(fall_time_interval))
        elif elapsed_time>60 and fall_add_flag==2:
            fall_add_flag=3
            fall_time_interval /=2
            pygame.time.set_timer(FALL, int(fall_time_interval))
            
    def rl_shift(self,direction):
        block_pos_list=[]
        stop_flag=False
        #壁の左右を超えない設定
        if direction == "r":
            range_j = range(10, 0, -1)
        elif direction == "l":
            range_j = range(1, 11)
        else:
            return
        for i in range(19, -1, -1):
            for j in range_j:
                if player_board.board[i][j]>0 :
                    block_pos_list.append((i,j))
                    if direction=="r" and player_board.board[i][j+1]==-1:
                        stop_flag=True
                    elif  direction=="l" and player_board.board[i][j-1]==-1:
                        stop_flag=True
        if not stop_flag:
            #左右移動
            for i,j in block_pos_list:
                if direction=="r":
                    temp=player_board.board[i][j]
                    player_board.board[i][j]=0
                    player_board.board[i][j+1]=temp
                    
                elif direction=="l":
                    temp=player_board.board[i][j]
                    player_board.board[i][j]=0
                    player_board.board[i][j-1]=temp
    
    def rotate(self,direction):
        block_pos_list=[]
        for i in range(19, -1, -1):
            for j in range(1, 11):
                if player_board.board[i][j]>0 :
                    block_pos_list.append((i,j))
        #左上を求める
        upper=block_pos_list[0][0]
        left=block_pos_list[0][1]
        for pos in block_pos_list:
            if pos[0]<upper:
                upper=pos[0]
            if pos[1]<left:
                left=pos[1]
        left_upper=(upper,left-1)

        #左上を起点に4*4行列をつくる
        block=[]
        for i in range(4):
            row=[]
            for j in range(4):
                if player_board.board[left_upper[0]+i][left_upper[1]+j]>0 :
                    row.append(player_board.board[left_upper[0]+i][left_upper[1]+j])
                else:
                    row.append(0)
            block.append(row)

        #上下変更と行列の転置で回転を表現
        rotated_block = []
        if direction=="r":
            #上下変更
            block=block[::-1]
            #転置
            num_columns = len(block[0])
            for i in range(num_columns):
                row = []
                for r in block:
                    row.append(r[i])
                rotated_block.append(row)
        elif direction=="l":
            #転置
            t = []
            num_columns = len(block[0])
            for i in range(num_columns):
                row = []
                for r in block:
                    row.append(r[i])
                t.append(row)
            #上下変更
            rotated_block=t[::-1]

        #衝突判定（回転後のボード座標に-1がないか）
        stop_flag=False
        for i in range(4):
            for j in range(4):
                if rotated_block[i][j]>0 and player_board.board[left_upper[0]+i][left_upper[1]+j]==-1 :
                    stop_flag=True

        if not stop_flag:
            #回転を反映
            for i,j in block_pos_list:
                player_board.board[i][j]=0 
            for i in range(4):
                for j in range(4):
                    if direction=="r":
                        #行を-1補正
                        player_board.board[left_upper[0]+i-1][left_upper[1]+j]=rotated_block[i][j]
                    elif direction=="l":
                        #列を+1補正
                        player_board.board[left_upper[0]+i][left_upper[1]+j+1]=rotated_block[i][j]
    
    def check_line(self):
        clear_flag=True
        #行にブロックがそろっているか
        for i in range(20):
            clear_flag=True
            for j in range(1, 11):
                if not fixed_board.board[i][j]>0:
                    clear_flag=False
            if clear_flag:
                #行の消去と追加
                fixed_board.board.pop(i)
                player_board.board.pop(i)
                row=[0]*12
                row.insert(0,-1)
                row.append(-1)
                fixed_board.board.insert(0,row)
                player_board.board.insert(0,row)                
                    
    def draw_gameboard(self):
        grid=GRID
        start_x,start_y=(WIDTH-grid*12)/2,(HEIGHT-grid*22)/2
        for i in range(22):
            #横線
            pygame.draw.line(window, WHITE, (start_x,start_y+i*grid),(start_x+(12*grid),start_y+i*grid), 1)
        for i in range(13):
            #縦線
            pygame.draw.line(window, WHITE, (start_x+i*grid,start_y),(start_x+i*grid,start_y+21*grid), 1)
        #壁の描画
        for i in range(21):
            pygame.draw.rect(window,WHITE, pygame.Rect(start_x, start_y+i*grid, grid-2, grid-2))
            pygame.draw.rect(window,WHITE, pygame.Rect(start_x+(11*grid), start_y+i*grid, grid-2, grid-2))
        for i in range(12):
            pygame.draw.rect(window,WHITE, pygame.Rect(start_x+i*grid, start_y+20*grid, grid-2, grid-2))
            
    def draw_blocks(self,board):
        #ボードの配列を受け取って画面に反映させる
        for i in range(21):
            for j in range(12):
                if board.board[i][j]>0:
                    color=blocks.get_block_color(board.board[i][j])
                    grid=GRID
                    start_x,start_y=(WIDTH-grid*12)/2,(HEIGHT-grid*22)/2
                    center_x=start_x+grid/2+grid*j
                    center_y=start_y+grid/2+grid*i
                    pygame.draw.circle(window,color,(center_x,center_y),13,0)

    def check_gameover(self):
        over_flag=False
        for j in range(1,11):
            if fixed_board.board[3][j]>0:
                over_flag=True
        if over_flag:
            print("gameover")
            global flag
            flag="GAMEOVER"

    def draw_gameover(self):
        font = pygame.font.Font(None, 72)  
        text = font.render("Game Over!", True, (255, 255, 255))  
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  
        rounded_rect_surface = pygame.Surface((400, 200), pygame.SRCALPHA)
        pygame.draw.rect(rounded_rect_surface, (0, 0, 255, 128), (0, 0, 400, 200), border_radius=20)
        rounded_rect_rect = rounded_rect_surface.get_rect(center=(WIDTH // 2, HEIGHT//2))
        window.blit(rounded_rect_surface, rounded_rect_rect)
        window.blit(text, text_rect)

pygame.init()
pygame.display.set_caption("FallingBlocks")
window=pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

#インスタンス化
fixed_board=Board()
player_board=Board()
blocks=Blocks()
game=GameSystem()

#落下時間ごとのイベント
FALL = pygame.USEREVENT + 1
fall_add_flag=0
fall_time_interval=1000
pygame.time.set_timer(FALL, fall_time_interval)
start_time=pygame.time.get_ticks()
flag="GAME"
def main():
   
    while True:
        events=pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key==pygame.K_RIGHT:
                    game.rl_shift("r")
                elif event.key==pygame.K_LEFT:
                    game.rl_shift("l")
                elif event.key==pygame.K_DOWN:
                    game.rotate("l")
                elif event.key==pygame.K_UP:
                    game.rotate("r")
                
            elif event.type==FALL:
                game.falling_block()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            game.falling_block()

        if flag=="GAME":
            current_time = pygame.time.get_ticks()
            game.falling_speed_manage(current_time)
            window.fill(BLACK)
            game.draw_gameboard()
            game.draw_blocks(player_board)
            game.draw_blocks(fixed_board)
            game.generate_block()
            game.check_line()
            game.check_gameover()
            pygame.display.flip()
            
        elif flag=="GAMEOVER":
            window.fill(BLACK)
            game.draw_gameover()
            pygame.display.flip()
        clock.tick(FPS)
if __name__ == "__main__":
    main()