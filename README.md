# DesignPattern_Dinosaur_Game
설계패턴 Dinosaur Game Refactoring

## Class Description
1. DinoState : 상태 패턴의 추상 크래스, 공룡의 상태(달리기, 앉기, 점프하기)를 나타내는 구체적인 상태 클래스들의 부모 클래스
- handle_input(dino, userInput): 상태 전환을 처리하는 메서드.

- update(dino): 상태 업데이트를 처리하는 메서드.

- enter(dino): 상태에 진입할 때의 초기화 작업을 처리하는 메서드.

2. RunningState, DuckingState, JumpingState: DinoState를 상속받는 구체적인 상태 클래스들로, 각기 다른 공룡의 상태를 나타냅니다.

- enter(dino): 상태에 진입할 때 초기화 작업을 수행합니다.

- handle_input(dino, userInput): 상태 전환을 처리합니다.

- update(dino): 상태 업데이트를 처리합니다.

3. Dinosaur: 공룡 클래스. 상태 패턴을 사용하여 공룡의 상태를 관리합니다.

- 속성:

  - X_POS, Y_POS, Y_POS_DUCK, JUMP_VEL: 공룡의 위치와 점프 속도.
  
  - duck_img, run_img, jump_img: 공룡의 이미지 리스트.

  - step_index, image, dino_rect, state: 공룡의 현재 상태와 이미지 정보.

- 메서드:

  - __init__(): 공룡 객체를 초기화합니다.

  - set_state(state): 공룡의 상태를 설정합니다.

  - update(userInput): 상태를 업데이트합니다.

  - draw(SCREEN): 공룡을 화면에 그립니다.

4. ObstacleUpdateStrategy: 전략 패턴의 추상 클래스. 장애물의 업데이트 로직을 정의합니다.

- update(obstacle): 장애물을 업데이트하는 메서드.

5. DefaultUpdateStrategy: ObstacleUpdateStrategy를 상속받는 클래스. 기본 장애물 업데이트 로직을 구현합니다.

- update(obstacle): 장애물의 위치를 업데이트합니다.

6. ObstacleFactory: 팩토리 패턴을 사용하여 장애물을 생성하는 클래스.

- create_obstacle(obstacle_type): 주어진 타입에 따라 장애물 객체를 생성합니다.

7. Obstacle: 장애물 클래스. 모든 장애물의 기본 클래스입니다.

- 속성:
  - image, type, rect, update_strategy: 장애물의 이미지, 타입, 사각형 영역, 업데이트 전략.

- 메서드:
  
  - __init__(image, type, update_strategy): 장애물 객체를 초기화합니다.

  - update(): 장애물을 업데이트합니다.

  - draw(SCREEN): 장애물을 화면에 그립니다.

8. SmallCactus, LargeCactus, Bird: Obstacle 클래스를 상속받는 구체적인 장애물 클래스들로, 각기 다른 종류의 장애물을 나타냅니다.

- __init__(image): 특정 타입의 장애물 객체를 초기화합니다.

9. Cloud: 구름 클래스. 구름 객체를 관리합니다.

- 속성:

  - x, y, image, width: 구름의 위치와 이미지 정보.

- 메서드:

  - __init__(): 구름 객체를 초기화합니다.

  - update(): 구름의 위치를 업데이트합니다.

  - draw(SCREEN): 구름을 화면에 그립니다.

## 클래스 다이어그램

![alt text](image.png)

