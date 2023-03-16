import numpy as np
import copy as deepcopy 
from datetime import datetime
import random
import math
xStart = 1
yStart = 1 
goal = (1,1)
def heuristic(a,b):
    return math.dist(a, b)
class State():
    def __init__(self, board, position, orientation, steps, h):
        self.board = board #cấu trúc bảng game
        self.position = position #vị trí ô của khối
        self.orientation = orientation #hướng của khối (ngang/dọc)
        self.steps = steps #số bước cần thiết để đến trạng thái này
        self.h = h #khoảng cách heuristic đến trạng thái đích

class Node():
    def __init__(self, state, parent=None, child=None):
        self.state = state #trạng thái
        self.parent = parent #nút cha
        
        self.child = child #con trỏ đến nút con
        self.value = 0 #giá trị trung bình khi thực hiện di chuyển đến trạng thái này
        self.visits = 0 #số lượt thăm nút này

# Bước 2: Tạo cây Monte Carlo Tree
def create_tree(board, goal ,init_position=(xStart,yStart)):
    # Khởi tạo trạng thái ban đầu và nút gốc của cây
    init_orientation = "v"
    init_state = State(board, init_position, init_orientation, 0, heuristic(init_position, goal))
    root = Node(init_state)
    return root

# Bước 3: Mở rộng nút lá bằng các phép di chuyển có thể có
def expand_node(node, goal):
    board = deepcopy(node.state.board)
    position = node.state.position
    orientation = node.state.orientation
    legal_actions = []
    if position[1] > 0 and board[position[0]][position[1] - 1] != "0":
        legal_actions.append("L")
    if position[1] < len(board[0]) - 1 and board[position[0]][position[1] + 1] != "0":
        legal_actions.append("R")
    if position[0] > 0 and board[position[0] - 1][position[1]] != "0":
        if orientation == "h" or orientation == "v" and board[position[0] - 2][position[1]] == "0":
            legal_actions.append("U")
    if position[0] < len(board) - 2 and board[position[0] + 2][position[1]] != "0":
        if orientation == "h" or orientation == "v" and board[position[0] + 2][position[1]] == "0":
            legal_actions.append("D")

    actions = legal_actions #các hành động có thể có để mở rộng
    for action in actions:
        new_state = execute_action(node.state, action, goal) #trạng thái mới sau khi di chuyển
        child_node = Node(new_state, parent=node) #tạo nút con với trạng thái mới và nút cha là nút đang xét
        node.child = child_node #thêm nút con vào cây
    return

# Bước 5: Thực hiện phép di chuyển và trả về trạng thái mới uiooooo
def execute_action(state, action, goal):
    new_board = deepcopy(state.board) #copy lại bảng game
    position = state.position #ở vị trí này, di chuyển đến vị trí khác
    orientation = state.orientation #hướng hiện tại
    steps = state.steps + 1 #số bước đi + 1 khi di chuyển đến trạng thái mới
    if action == "L": #di chuyển sang trái
        if orientation == "h": #nếu khối đang nằm ngang (một phần của khối ở vị trí bên trái)
            x, y = position[0], position[1] 
            new_x, new_y = x, y - 2 #di 2 ô về bên phải (hướng ngang sang trái)
            if new_y < 0: 
                return None
            if new_board[x][new_y] == "0" or new_board[x][new_y + 1] == "0": #không di chuyển tới ô trống
                return None
        elif orientation == "v": #nếu khối đang nằm dọc (một phần của khối ở vị trí bên trái)
            x, y = position[0], position[1]
            new_x, new_y = x, y - 1 #di 1 ô về bên trái (hướng dọc sang trái)
            if new_y < 0 or new_y > len(new_board[0])-1:
                return None
            if new_board[x][new_y] == "0": #không di chuyển tới ô trống
                return None
            if new_x + 1 <= len(new_board) - 1 and new_board[new_x][new_y] == "0" and new_board[new_x + 1][new_y] == "0": #không di chuyển tới ô trống
                return None
        new_board[position[0]][position[1] - 1] = "S" #trong tình huống di chuyển thành công, trạng thái mới sẽ là "S" (start)
        new_board[position[0]][position[1] + 1] = "S"
        new_board[new_x][new_y] = "B"
        new_board[new_x][new_y + 1] = "B"
        new_position = (new_x, new_y + 1) #Nếu khối di chuyển thành công (không gặp lỗi), trả về trạng thái mới
        return State(new_board, new_position, orientation, steps, heuristic(new_position, goal)) 
    elif action == "R": #tương tự hướng sang phải
        if orientation == "h":
            x, y = position[0], position[1]
            new_x, new_y = x, y + 2
            if new_y > len(new_board[0])-1:
                return None
            if new_board[x][new_y] == "0" or new_board[x][new_y - 1] == "0":
                return None
        elif orientation == "v":
            x, y = position[0], position[1]
            new_x, new_y = x, y + 1
            if new_y > len(new_board[0])-1 or new_y < 0:
                return None
            if new_board[x][new_y] == "0":
                return None
            if new_x + 1 <= len(new_board) - 1 and new_board[new_x][new_y] == "0" and new_board[new_x + 1][new_y] == "0":
                return None
        new_board[position[0]][position[1]] = "S"
        new_board[position[0]][position[1] + 2] = "S"
        new_board[new_x][new_y] = "B"
        new_board[new_x][new_y - 1] = "B"
        new_position = (new_x, new_y - 1)
        return State(new_board, new_position, orientation, steps, heuristic(new_position, goal))
    elif action == "U": #hướng lên trên
        if orientation == "h":
            x, y = position[0], position[1]
            new_x, new_y = x - 2, y
            if new_x < 0:
                return None
            if new_board[new_x][y] == "0" or new_board[new_x + 1][y] == "0":
                return None
        elif orientation == "v": #nếu khối đang ở trạng thái dọc thì khối sẽ di chuyển lên trên 2 dòng (2 ô trên)
            x, y = position[0], position[1]
            new_x, new_y = x - 1, y
            if new_x < 0 or new_x > len(new_board) - 1:
                return None
            if new_board[new_x][new_y] == "0":
                return None
            if y + 1 <= len(new_board[0]) - 1 and new_board[new_x][new_y] == "0" and new_board[new_x][new_y + 1] == "0":
                return None
        new_board[position[0] - 1][position[1]] = "S"
        new_board[position[0] + 1][position[1]] = "S"
        new_board[new_x][new_y] = "B"
        new_board[new_x + 1][new_y] = "B"
        new_position = (new_x + 1, new_y)
        return State(new_board, new_position, orientation, steps, heuristic(new_position, goal))
    elif action == "D": #hướng xuống dưới
        if orientation == "h":
            x, y = position[0], position[1]
            new_x, new_y = x + 2, y
            if new_x > len(new_board) - 1:
                return None
            if new_board[new_x][y] == "0" or new_board[new_x - 1][y] == "0":
                return None
        elif orientation == "v": #nếu khối đang ở trạng thái dọc thì khối sẽ di chuyển xuống dưới 2 dòng (2 ô dưới)
            x, y = position[0], position[1]
            new_x, new_y = x + 1, y
            if new_x > len(new_board) - 1 or new_x < 0:
                return None
            if new_board[new_x][new_y] == "0":
                return None
            if y + 1 <= len(new_board[0]) - 1 and new_board[new_x - 1][new_y] == "0" and new_board[new_x - 1][new_y + 1] == "0":
                return None
        new_board[position[0]][position[1]] = "S"
        new_board[position[0] + 2][position[1]] = "S"
        new_board[new_x][new_y] = "B"
        new_board[new_x - 1][new_y] = "B"
        new_position = (new_x - 1, new_y)
        return State(new_board, new_position, orientation, steps, heuristic(new_position, goal))

# Bước 4: Áp dụng thuật toán UCT (bắt đầu từ nút gốc để tìm ra nút con để mở rộng tiếp theo) uioooo
def uct(node, c):
    if node.visits == 0:
        return float("inf")
    return (node.value / node.visits) + c * np.sqrt(np.log(node.parent.visits) / node.visits)

# Bước 7: Lặp lại quá trình để tìm ra đường đi ngắn nhất đến trạng thái đích hoặc hết giới hạn thời gian
def mcts(board, goal, time_limit=60.0, iteration_limit=1000, exploration_constant=1 / np.sqrt(2)):
    root = create_tree(board, goal)
    start = datetime.now()
    while (datetime.now() - start).total_seconds() < time_limit:
        node = root
        path = [node]
        # Chọn nút lá tiếp theo để mở rộng
        while node.child is not None:
            uct_scores = [uct(child, exploration_constant) for child in node.child]
            selected_child = node.child[np.argmax(uct_scores)]
            path.append(selected_child)
            node = selected_child
        # Mở rộng nút để tìm kiếm các trạng thái mới
        expand_node(node, goal)
        # Chọn trạng thái ngẫu nhiên để tính toán giá trị
        result_state = random_simulation(node)
        
        # Cập nhật lại giá trị trung bình và số lượt thăm nút của các nút cha liên quan trong cây
        for node in reversed(path):
            node.visits += 1
            node.value += (result_state.steps - node.state.steps + node.state.h - result_state.h) / (len(path) - 1)
    # Trả về đường đi ngắn nhất đến trạng thái đích
    goal_node = root
    while goal_node.state.position != goal:
        uct_scores = [uct(child, exploration_constant) for child in goal_node.child]
        selected_child = goal_node.child[np.argmax(uct_scores)]
        goal_node = selected_child
    solution_path = []
    while goal_node.parent is not None:
        solution_path.append(goal_node.state)
        goal_node = goal_node.parent
    solution_path.reverse()
    return solution_path

# Bước 6: Thực hiện mô phỏng ngẫu nhiên để chọn trạng thái tiếp theo và trả về trạng thái cuối cùng
def random_simulation(node):
    board = deepcopy(node.state.board)
    steps = node.state.steps
    position = node.state.position
    orientation = node.state.orientation
    goal_pos = goal
    h = heuristic(position, goal_pos)
    while position != goal_pos:
        legal_actions = []
        if position[1] > 0 and board[position[0]][position[1] - 1] != "0":
            legal_actions.append("L")
        if position[1] < len(board[0]) - 1 and board[position[0]][position[1] + 1] != "0":
            legal_actions.append("R")
        if position[0] > 0 and board[position[0] - 1][position[1]] != "0":
            if orientation == "h" or orientation == "v" and board[position[0] - 2][position[1]] == "0":
                legal_actions.append("U")
        if position[0] < len(board) - 2 and board[position[0] + 2][position[1]] != "0":
            if orientation == "h" or orientation == "v" and board[position[0] + 2][position[1]] == "0":
                legal_actions.append("D")
        
        if len(legal_actions) == 0:
            return State(board, position, orientation, steps, h)
        
        action = random.choice(legal_actions)
        new_state = execute_action(State(board, position, orientation, 0, heuristic(position, goal_pos)), action, goal_pos)
        
        if new_state is None:
            return State(board, position, orientation, steps, h)
        else:
            board = new_state.board
            position = new_state.position
            orientation = new_state.orientation
            steps = new_state.steps
    return State(board, position, orientation, steps, h)
