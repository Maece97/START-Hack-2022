import { defineStore } from 'pinia';
import { ChatMessage } from '@/interfaces/chat';
import { createChatMessage, getChatMessage } from '@/_services/chat';

interface Sentiment {
  compound: number;
  negative: number;
  neutral: number;
  overallSentiment: string;
  positive: number;
}

interface Timeline {
  time: string;
  value: number;
}

interface WordCloud {
  text: string;
  value: number;
}

type ChatState = {
  chat: ChatMessage[];
  sentiment: Sentiment;
  timeline: Timeline[];
  wordCloud: WordCloud[];
};

// const messages = [
//   {
//     message: 'Hi, FIRST!',
//     timestamp: 1,
//     username: 'elrak',
//   },
//   {
//     message: 'Hey 😀😀😀😀😀😀😀😀😀',
//     timestamp: 1,
//     username: 'proGamerLPHD',
//   },
//   {
//     message: '😀😀😀y',
//     timestamp: 1,
//     username: 'yoloTV',
//   },
//   {
//     message: 'YOOYOYOYOYOOYYO',
//     timestamp: 1,
//     username: 'FifaPro2008',
//   },
//   {
//     message: 'Moin',
//     timestamp: 2,
//     username: 'germanLetsplayer',
//   },
//   {
//     message: 'Heyyyyyyy, heyyyy',
//     timestamp: 2,
//     username: 'proGamerLPHD',
//   },
//   {
//     message: 'Hi Kriiis ❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️',
//     timestamp: 2,
//     username: 'zuluuuuu',
//   },
//   {
//     message: 'Bro',
//     timestamp: 3,
//     username: 'footballguy12',
//   },
//   {
//     message: '🆒🆒🆒🆒🆒🆒🆒🆒🆒🆒🆒',
//     timestamp: 4,
//     username: 'proGamerLPHD',
//   },
//   {
//     message: '💩💩💩💩💩💩💩💩💩💩💩💩',
//     timestamp: 5,
//     username: 'gamer12',
//   },
//   {
//     message: 'FIFA FIFA',
//     timestamp: 10,
//     username: 'ronaldo56',
//   },
//   {
//     message: 'GOOOOOOOOOOOOOOOOO',
//     timestamp: 6,
//     username: 'ChessLegendChess',
//   },
//   {
//     message: 'Hey Kris 😎',
//     timestamp: 8,
//     username: 'Marcel#1337',
//   },
//   {
//     message: 'Hiii',
//     timestamp: 9,
//     username: 'jkfklofsds',
//   },
//   {
//     message: '😎😎😎😎😎😎😎😎😎😎😎😎',
//     timestamp: 10,
//     username: 'TheDoooooor543',
//   },
//   {
//     message: "Hi Kris let's win some games",
//     timestamp: 12,
//     username: 'DesignRuben69',
//   },
//   {
//     message: '🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸',
//     timestamp: 14,
//     username: 'Marcel#1337',
//   },
//   {
//     message: 'Today it is raining',
//     timestamp: 12,
//     username: 'umbrellaMan1000',
//   },
//   {
//     message: 'START HACK!!!!!!!',
//     timestamp: 14,
//     username: 'Daniel',
//   },
//   {
//     message: '🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡',
//     timestamp: 13,
//     username: 'proGamerLPHD',
//   },
//   {
//     message: "Let's play clash royal",
//     timestamp: 19,
//     username: 'ML_Alex007',
//   },
//   {
//     message: 'Ultimate TEAM',
//     timestamp: 20,
//     username: 'umbrellaMan1000',
//   },
//   {
//     message: '⚽⚽⚽⚽⚽⚽⚽',
//     timestamp: 21,
//     username: 'ronaldo56',
//   },
//   {
//     message: 'accept my firend request',
//     timestamp: 21,
//     username: 'DesignRuben69',
//   },
//   {
//     message: 'FIFA',
//     timestamp: 22,
//     username: 'proGamerLPHD',
//   },
//   {
//     message: 'Kris is the best',
//     timestamp: 24,
//     username: 'KRISFAN2013',
//   },
//   {
//     message: 'This guy is hacking!!!!!!!!!',
//     timestamp: 26,
//     username: 'NotAHacker123',
//   },
//   {
//     message: 'Clash royal > FIFA',
//     timestamp: 28,
//     username: 'supercellfan34',
//   },
//   {
//     message: 'Shoot',
//     timestamp: 30,
//     username: 'gamer12',
//   },
//   {
//     message: '⚽⚽⚽⚽⚽⚽⚽⚽⚽⚽',
//     timestamp: 32,
//     username: 'KRISFAN2013',
//   },
//   {
//     message: 'Yes he is!',
//     timestamp: 37,
//     username: 'ronaldo56',
//   },
//   {
//     message: 'Troll!',
//     timestamp: 39,
//     username: 'NotAHacker123',
//   },
//   {
//     message: 'Nice play!',
//     timestamp: 44,
//     username: 'gamer12',
//   },
//   {
//     message: 'Hi Krisman!!!',
//     timestamp: 48,
//     username: 'Baker494',
//   },
//   {
//     message: 'Get the ball!',
//     timestamp: 52,
//     username: 'KRISFAN2013',
//   },
//   {
//     message: 'This was a goal!!!',
//     timestamp: 55,
//     username: 'supercellfan34',
//   },
//   {
//     message: 'You are bad!',
//     timestamp: 57,
//     username: 'NotAHacker123',
//   },
//   {
//     message: '😈😈😈😈😈😈😈😈',
//     timestamp: 58,
//     username: 'ML_Alex007',
//   },
//   {
//     message: 'Drink some water man!',
//     timestamp: 59,
//     username: 'waterman',
//   },
//   {
//     message: 'Long live the lost ball',
//     timestamp: 60,
//     username: 'Tomuchsad',
//   },
//   {
//     message: 'Chill',
//     timestamp: 62,
//     username: 'KRISFAN2013',
//   },
//   {
//     message: 'For sure!',
//     timestamp: 64,
//     username: 'gamer12',
//   },
//   {
//     message: '🥶🥶🥶🥶',
//     timestamp: 64,
//     username: 'DesignRuben69',
//   },
//   {
//     message: 'GO Sports!',
//     timestamp: 68,
//     username: 'proGamerLPHD',
//   },
//   {
//     message: 'I really enjoy your entertaining content',
//     timestamp: 72,
//     username: 'StreamLover99',
//   },
//   {
//     message: 'Whoah, that not cool! You went too far there. That was shit!',
//     timestamp: 76,
//     username: 'Hackerman123',
//   },
//   {
//     message: 'Yeah that was really uncalled for!',
//     timestamp: 77,
//     username: 'StreamLover99',
//   },
//   {
//     message: 'NOOOOOOO',
//     timestamp: 78,
//     username: 'BigBear43',
//   },
//   {
//     message: 'Dont be mean!',
//     timestamp: 79,
//     username: 'StreamLover99',
//   },
//   {
//     message: 'That is bad!',
//     timestamp: 79,
//     username: 'StreamLover99',
//   },
//   {
//     message: 'Dont insult',
//     timestamp: 83,
//     username: 'BigBear43',
//   },
//   {
//     message: 'It is just a game, no need to insult people!',
//     timestamp: 80,
//     username: 'BigBear43',
//   },
//   {
//     message: 'WHAT',
//     timestamp: 82,
//     username: 'BigBear43',
//   },
//   {
//     message: 'Dont insult',
//     timestamp: 83,
//     username: 'BigBear43',
//   },
//   {
//     message: 'It is just a game, no need to insult people!',
//     timestamp: 83,
//     username: 'BigBear43',
//   },
//   {
//     message: 'Thats not!',
//     timestamp: 83,
//     username: 'BigBear43',
//   },
//   {
//     message: 'bad',
//     timestamp: 85,
//     username: 'BigBear43',
//   },
//   {
//     message: ';(',
//     timestamp: 85,
//     username: 'BigBear43',
//   },
//   {
//     message: 'OK',
//     timestamp: 88,
//     username: 'PRFGUY',
//   },
//   {
//     message: 'Well, done! Nice Goal',
//     timestamp: 95,
//     username: 'StreamLover99',
//   },
//   {
//     message: 'Damn man! What a superb shot',
//     timestamp: 96,
//     username: 'BigBear43',
//   },
//   {
//     message: 'That showed some great skill! I love you!',
//     timestamp: 97,
//     username: 'StreamLover99',
//   },
//   {
//     message: 'Thats a nice attitude!',
//     timestamp: 98,
//     username: 'Hackerman123',
//   },
//   {
//     message: 'Yeah he sadly really is not the best player :/',
//     timestamp: 108,
//     username: 'StreamLover99',
//   },
//   {
//     message: 'Maybe you could teach him some of your tricks :)',
//     timestamp: 109,
//     username: 'Hackerman123',
//   },
//   {
//     message: 'Well then go ahead and win this game!',
//     timestamp: 117,
//     username: 'BigBear43',
//   },
//   {
//     message: 'Indeed maybe you are not as good as you thought after all',
//     timestamp: 122,
//     username: 'MoSalah65',
//   },
//   {
//     message: 'No Kris is the best player in the world!',
//     timestamp: 123,
//     username: 'StreamLover99',
//   },
//   {
//     message: 'Congratulations on the nice game!',
//     timestamp: 128,
//     username: 'Hackerman123',
//   },
//   {
//     message: 'GG! Well played!',
//     timestamp: 129,
//     username: 'StreamLover99',
//   },
// ];

// eslint-disable-next-line import/prefer-default-export
export const useChatStore = defineStore('chat', {
  state: (): ChatState =>
    // eslint-disable-next-line implicit-arrow-linebreak
    ({
      chat: [],
      sentiment: {
        compound: 0,
        negative: 0,
        neutral: 0,
        overallSentiment: 'Neutral',
        positive: 0,
      },
      timeline: [
        { time: '1', value: 0 },
        { time: '2', value: 0 },
      ],
      wordCloud: [],
    }),
  getters: {
    getChat(): ChatMessage[] {
      return this.chat;
    },
    getSentiment(): Sentiment {
      return this.sentiment;
    },
    getTimeline(): Timeline[] {
      return this.timeline;
    },
    getWordCloud(): WordCloud[] {
      const relevant = this.wordCloud.filter((x) => x.value !== 0);
      function absoluteValueComparison(a: WordCloud, b: WordCloud) {
        if (Math.abs(a.value) < Math.abs(b.value)) {
          return 1;
        }
        if (Math.abs(a.value) > Math.abs(b.value)) {
          return -1;
        }
        if (a.value < b.value) {
          return 1;
        }
        if (a.value > b.value) {
          return -1;
        }
        return 0;
      }
      return relevant.sort(absoluteValueComparison).slice(0, 5);
    },
  },
  actions: {
    async getChatMessages() {
      const m = await getChatMessage();
      this.chat = m;
    },
    // any amount of arguments, return a promise or not
    async sendChatMessage(message: string, startTime: number, username?: string) {
      let usernameNew = username?.trim();
      if (usernameNew === '') {
        usernameNew = undefined;
      }

      const chatMessage: ChatMessage = {
        message,
        timestamp: Date.now(),
        startTime,
        username: usernameNew || `Anon${Math.floor(Math.random() * (999 - 100) + 100)}`,
      };
      const response = await createChatMessage(chatMessage);
      // this.sentiment = {
      //   overallSentiment: response.avg_sentiment.overall_sentiment,
      //   ...response.avg_sentiment,
      // };

      // this.timeline = [];
      // // eslint-disable-next-line no-restricted-syntax
      // for (const [key, value] of Object.entries(response.timeline)) {
      //   this.timeline.push({
      //     time: key,
      //     // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      //     // @ts-ignore
      //     value,
      //   });
      // }

      // this.wordCloud = [];
      // eslint-disable-next-line no-restricted-syntax
      // for (const [key, value] of Object.entries(response.sentence_map)) {
      //   this.wordCloud.push({
      //     text: key,
      //     // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      //     // @ts-ignore
      //     value,
      //   });
      // }

      // this.chat.push(chatMessage);
    },
    init() {
      // Create WebSocket connection.
      const socket = new WebSocket(
        `${process.env.VUE_APP_WEBSOCKET_URL || 'ws://localhost:8080'}/ws`,
      );

      // Connection opened
      socket.addEventListener('open', (event) => {
        // socket.send('Hello Server!');
      });

      // Listen for messages
      socket.addEventListener('message', (event) => {
        const data = JSON.parse(event.data);

        this.sentiment = {
          overallSentiment: data.result.avg_sentiment.overall_sentiment,
          ...data.result.avg_sentiment,
        };

        this.timeline = [
          { time: '1', value: 0 },
          { time: '2', value: 0 },
        ];
        // eslint-disable-next-line no-restricted-syntax
        for (const [key, value] of Object.entries(data.result.timeline)) {
          this.timeline.push({
            time: key,
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
            value,
          });
        }

        this.chat.push(data.message);
      });
    },
    // async autoChatMessage(time: number, timestamp: number, callback: any) {
    //   const m = messages.filter((x) => x.timestamp === time);
    //   let counter = 0;
    //   const min = 500;
    //   const max = 1500;
    //   // eslint-disable-next-line no-restricted-syntax
    //   for (const x of m) {
    //     setTimeout(() => {
    //       this.sendChatMessage(x.message, timestamp, x.username);
    //       callback();
    //     }, counter * Math.random() * (max - min) + min);
    //     counter += 1;
    //   }
    // },
  },
});
