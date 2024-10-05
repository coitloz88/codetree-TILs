import sys
from collections import deque
input = sys.stdin.readline

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

R, C, K = map(int, input().split())
R += 3

golems = [(map(int, input().split())) for _ in range(K)]
forest = [[-1] * C for _ in range(R)]

def check_range(r, c):
    return 0 <= r < R and 0 <= c < C

def check_movable(r, c, dr, dc):
    for ddr, ddc in zip(dr, dc):
        nr, nc = r + ddr, c + ddc
        if (not check_range(nr, nc)) or forest[nr][nc] >= 0:
            return False
    return True

queue = deque([])
forest_middle = {}
answer = 0

# 각 골렘 전체 이동
for i, (start, exit_dir) in enumerate(golems):
    r, c = 0, start - 1 # 시작 중심 좌표

    # i번째 골렘 이동 로직 루프
    while True:
        if (check_movable(r, c, [1, 2, 1], [-1, 0, 1])):
            r, c = r + 1, c
        elif (check_movable(r, c, [-1, 0, 1, 1, 2], [-1, -2, 1, -2, -1])):
            r, c = r, c - 1
            exit_dir = (exit_dir - 1) % 4 # 반시계 방향으로 출구 회전
        elif (check_movable(r, c, [-1, 0, 1, 1, 2], [1, 2, 1, 2, 1])):
            r, c = r, c + 1
            exit_dir = (exit_dir + 1) % 4 # 시계 방향으로 출구 회전
        else:
            break # 어디로도 이동 불가한 경우 골렘 이동 중지

    if r < 4: # 골렘이 맵 안으로 완전히 못 들어온 경우 숲 초기화
        forest = [[-1] * C for _ in range(R)] # 숲 초기화
        queue = deque([])
        forest_middle = {}
        continue # bfs 수행 없이 다음 골렘으로 넘어감
    
    forest[r][c] = i
    forest_middle[i] = (r, c, exit_dir)
    for d_i in range(4):
        nr, nc = r + dr[d_i], c + dc[d_i]
        if check_range(nr, nc):
            forest[nr][nc] = i
    # print(forest)

    # TODO: 각 요정 최종 이동 후 행 번호 누적 (BFS)
    queue.append((r, c, exit_dir)) # 요정 시작 위치
    visited = []
    max_row = 0
    while queue:
        cur_loc = queue.popleft()
        
        exit = (cur_loc[0] + dr[cur_loc[2]], cur_loc[1] + dc[cur_loc[2]])
        max_row = max(max_row, cur_loc[0] + 1 - 2)

        for dir_idx in range(4):
            nr, nc = exit[0] + dr[dir_idx], exit[1] + dc[dir_idx]
            if check_range(nr, nc) and forest[nr][nc] >= 0 and forest[nr][nc] != i and forest_middle[forest[nr][nc]] not in visited:
                queue.append(forest_middle[forest[nr][nc]])
                visited.append(forest_middle[forest[nr][nc]])
    answer += max_row

print(answer)