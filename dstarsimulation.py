import pygame
import heapq
import sys
import random

pygame.init()

# ================= CONFIG =================
GRID_SIZE = 30
CELL = 20
GRID_PIX = GRID_SIZE * CELL

SCREEN = pygame.display.set_mode((1200,700))
pygame.display.set_caption("D* Lite Stable Visualizer")

WHITE=(255,255,255)
BLACK=(0,0,0)
GRAY=(200,200,200)
GREEN=(0,200,0)
RED=(220,50,50)
ORANGE=(255,165,0)
LIGHTBLUE=(170,220,255)
BTN=(70,130,180)
BTN_OFF=(150,150,150)

font=pygame.font.SysFont(None,24)

# ================= NODE =================
class Node:
    def __init__(self,r,c):
        self.r=r; self.c=c
        self.g=float("inf")
        self.rhs=float("inf")
        self.obstacle=False
    def __lt__(self,o): return False

# ================= D* LITE =================
class DStarLite:
    def __init__(self,grid,start,goal):
        self.grid=grid
        self.start=start
        self.goal=goal
        self.U=[]
        goal.rhs=0
        heapq.heappush(self.U,(self.key(goal),goal))

    def h(self,a,b):
        return abs(a.r-b.r)+abs(a.c-b.c)

    def key(self,n):
        return (min(n.g,n.rhs)+self.h(self.start,n),min(n.g,n.rhs))

    def neigh(self,n):
        d=[(1,0),(-1,0),(0,1),(0,-1)]
        out=[]
        for dr,dc in d:
            r,c=n.r+dr,n.c+dc
            if 0<=r<GRID_SIZE and 0<=c<GRID_SIZE:
                if not self.grid[r][c].obstacle:
                    out.append(self.grid[r][c])
        return out

    def update(self,u):
        if u!=self.goal:
            vals=[s.g+1 for s in self.neigh(u)]
            u.rhs=min(vals) if vals else float("inf")

        self.U=[(k,n) for (k,n) in self.U if n!=u]
        heapq.heapify(self.U)

        if u.g!=u.rhs:
            heapq.heappush(self.U,(self.key(u),u))

    # watchdog prevents infinite loop
    def compute(self, max_iter=10000):
        it=0
        while self.U and it<max_iter:
            it+=1
            k,u=heapq.heappop(self.U)

            if u.g>u.rhs:
                u.g=u.rhs
                for s in self.neigh(u):
                    self.update(s)
            else:
                u.g=float("inf")
                self.update(u)
                for s in self.neigh(u):
                    self.update(s)

    def path(self):
        if not self.start or not self.goal:
            return []

        p=[self.start]
        n=self.start

        while n!=self.goal:
            ns=self.neigh(n)
            if not ns: return []

            n=min(ns,key=lambda x:x.g)
            if n.g==float("inf"): return []

            p.append(n)

        return p

# ================= GRID =================
def new_grid():
    return [[Node(r,c) for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]

def reset_all():
    return new_grid(), None, None, None, None, []

grid, start, goal, planner, robot, path = reset_all()

# ================= BUTTONS =================
btn_next  = pygame.Rect(40,630,120,35)
btn_reset = pygame.Rect(200,630,120,35)
btn_rand  = pygame.Rect(360,630,120,35)

# ================= SAFE REPLAN =================
def replan():
    global planner, path
    if planner:
        planner.compute()
        path = planner.path()

# ================= DRAW =================
def draw_exec():
    surf=pygame.Surface((600,700))
    surf.fill(WHITE)

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            n=grid[r][c]
            rect=pygame.Rect(c*CELL,r*CELL,CELL,CELL)

            if n.obstacle: pygame.draw.rect(surf,BLACK,rect)
            elif n==start: pygame.draw.rect(surf,GREEN,rect)
            elif n==goal: pygame.draw.rect(surf,RED,rect)
            elif n==robot: pygame.draw.rect(surf,ORANGE,rect)

            pygame.draw.rect(surf,GRAY,rect,1)

    def b(rect,text,en=True):
        pygame.draw.rect(surf, BTN if en else BTN_OFF, rect)
        surf.blit(font.render(text,True,WHITE),(rect.x+10,rect.y+8))

    b(btn_next,"NEXT", planner is not None)
    b(btn_reset,"RESET", True)
    b(btn_rand,"RANDOM", True)

    return surf

def draw_map():
    surf=pygame.Surface((600,600))
    surf.fill((240,240,240))

    # reachable region
    if planner:
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                n=grid[r][c]
                if not n.obstacle and n.g!=float("inf"):
                    pygame.draw.rect(surf,LIGHTBLUE,(c*CELL,r*CELL,CELL,CELL))

    # obstacles
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c].obstacle:
                pygame.draw.rect(surf,BLACK,(c*CELL,r*CELL,CELL,CELL))

    # path
    for n in path:
        pygame.draw.rect(surf,GREEN,(n.c*CELL,n.r*CELL,CELL,CELL))

    for x in range(0,600,CELL):
        pygame.draw.line(surf,GRAY,(x,0),(x,600))
    for y in range(0,600,CELL):
        pygame.draw.line(surf,GRAY,(0,y),(600,y))

    return surf

# ================= LOOP =================
clock=pygame.time.Clock()

while True:
    clock.tick(30)

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit(); sys.exit()

        if e.type==pygame.MOUSEBUTTONDOWN:
            x,y=e.pos

            if x<600:
                # NEXT STEP
                if btn_next.collidepoint(x,y) and planner and path:
                    if robot and robot!=goal and len(path)>1:
                        robot = path[1]
                        planner.start = robot
                        start = robot
                        replan()

                # RESET
                elif btn_reset.collidepoint(x,y):
                    grid, start, goal, planner, robot, path = reset_all()

                # RANDOM OBSTACLES
                elif btn_rand.collidepoint(x,y):
                    for r in range(GRID_SIZE):
                        for c in range(GRID_SIZE):
                            grid[r][c].obstacle = random.random()<0.2
                    if start and goal:
                        planner = DStarLite(grid,start,goal)
                        robot = start
                        replan()

                # GRID CLICK
                elif y<GRID_PIX:
                    r=y//CELL; c=x//CELL
                    node=grid[r][c]

                    if not start:
                        start=node
                        robot=start

                    elif not goal and node!=start:
                        goal=node
                        planner=DStarLite(grid,start,goal)
                        replan()

                    elif node!=start and node!=goal:
                        node.obstacle=True

                        if planner:
                            planner.update(node)

                            # critical neighbor updates
                            for nb in planner.neigh(node):
                                planner.update(nb)

                            replan()

    exec_view=draw_exec()
    map_view=draw_map()

    SCREEN.fill(WHITE)
    SCREEN.blit(exec_view,(0,0))
    SCREEN.blit(map_view,(600,0))

    pygame.display.update()
