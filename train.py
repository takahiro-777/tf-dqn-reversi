import copy

from Reversi import Reversi
from dqn_agent import DQNAgent


if __name__ == "__main__":

    # parameters
    #n_epochs = 1000
    n_epochs = 5
    # environment, agent
    env = Reversi()

    # playerID
    playerID = [env.Black, env.White, env.Black]

    # player agent
    players = []
    # player[0]= env.Black
    players.append(DQNAgent(env.enable_actions, env.name, env.screen_n_rows, env.screen_n_cols))
    # player[1]= env.White
    players.append(DQNAgent(env.enable_actions, env.name, env.screen_n_rows, env.screen_n_cols))


    for e in range(n_epochs):
        # reset
        env.reset()
        terminal = False
        while terminal == False: # 1エピソードが終わるまでループ

            for i in range(0, len(players)):

                state = env.screen
                #print(state)
                targets = env.get_enables(playerID[i])

                exploration = (n_epochs - e + 20)/(n_epochs + 20)
                #exploration = 0.1

                if len(targets) > 0:
                    # どこかに置く場所がある場合

                    #すべての手をトレーニングする
                    for tr in targets:
                        tmp = copy.deepcopy(env)
                        tmp.update(tr, playerID[i])
                        #終了判定
                        win = tmp.winner()
                        end = tmp.isEnd()
                        #次の状態
                        state_X = tmp.screen
                        target_X = tmp.get_enables(playerID[i+1])
                        if len(target_X) == 0:
                            target_X = tmp.get_enables(playerID[i])

                        # 両者トレーニング
                        for j in range(0, len(players)):
                            reword = 0
                            if end == True:
                                if win == playerID[j]:
                                    # 勝ったら報酬1を得る
                                    reword = 1

                            players[j].store_experience(state, targets, tr, reword, state_X, target_X, end)
                            #print(state)
                            #print(state_X)
                            #if e > n_epochs*0.2:
                            #    players[j].experience_replay()


                    # 行動を選択
                    action = players[i].select_action(state, targets, exploration)
                    # 行動を実行
                    env.update(action, playerID[i])
                    # for log
                    loss = players[i].current_loss
                    Q_max, Q_action = players[i].select_enable_action(state, targets)
                    print("player:{:1d} | pos:{:2d} | LOSS: {:.4f} | Q_MAX: {:.4f} | Q_ACTION: {:.4f}".format(
                             playerID[i], action, loss, Q_max, Q_action))




                # 行動を実行した結果
                terminal = env.isEnd()

        for j in range(0, len(players)):
            if e > n_epochs*0.3:
                for k in range(25):
                    players[j].experience_replay()
            elif e > n_epochs*0.1:
                for k in range(5):
                    players[j].experience_replay()

        w = env.winner()
        print("EPOCH: {:03d}/{:03d} | WIN: player{:1d}".format(
                         e, n_epochs, w))


        # 保存は後攻のplayer2 を保存する。
        if e%50 == 0:
            players[1].save_model(e)
