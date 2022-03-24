import { defineStore } from 'pinia';
import { ChatMessage } from '@/interfaces/chat';
import { createChatMessage } from '@/_services/chat';

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

type ChatState = {
  chat: ChatMessage[];
  sentiment: Sentiment;
  timeline: Timeline[];
  wordCloud: [];
};

const messages = [
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 1,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 1,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 1,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 1,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 1,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 1,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 1,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 1,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 10,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 10,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 10,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 10,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 10,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 10,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 10,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 10,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 10,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 20,
    username: 'proGamerLPHD',
  },
  {
    message: 'I love you',
    timestamp: 20,
    username: 'proGamerLPHD',
  },
  {
    message: 'I love you',
    timestamp: 20,
    username: 'proGamerLPHD',
  },
  {
    message: 'I love you',
    timestamp: 20,
    username: 'proGamerLPHD',
  },
  {
    message: 'I love you',
    timestamp: 20,
    username: 'proGamerLPHD',
  },
  {
    message: 'I love you',
    timestamp: 20,
    username: 'proGamerLPHD',
  },
  {
    message: 'I love you',
    timestamp: 20,
    username: 'proGamerLPHD',
  },
  {
    message: 'I love you',
    timestamp: 30,
    username: 'proGamerLPHD',
  },
  {
    message: 'HI love you',
    timestamp: 30,
    username: 'proGamerLPHD',
  },
  {
    message: 'I love you',
    timestamp: 30,
    username: 'proGamerLPHD',
  },
  {
    message: 'I love you',
    timestamp: 30,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 30,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 30,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 30,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 40,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 40,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 40,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 40,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 40,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 40,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 40,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 50,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 50,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 50,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 50,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 50,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 50,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 50,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 50,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 50,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 60,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 60,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 60,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 60,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 60,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 60,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 70,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 70,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 70,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 70,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 70,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 70,
    username: 'proGamerLPHD',
  },
  {
    message: 'Heyyyyyyy, heyyyy babyyyy',
    timestamp: 70,
    username: 'proGamerLPHD',
  },
];

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
      timeline: [],
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
  },
  actions: {
    // any amount of arguments, return a promise or not
    async sendChatMessage(message: string, startTime: number, username?: string) {
      const chatMessage: ChatMessage = {
        message,
        timestamp: Date.now(),
        startTime,
        username: username || 'xxGamer2001xx',
      };
      const response = await createChatMessage(chatMessage);
      this.sentiment = {
        overallSentiment: response.avg_sentiment.overall_sentiment,
        ...response.avg_sentiment,
      };

      this.timeline = [];
      // eslint-disable-next-line no-restricted-syntax
      for (const [key, value] of Object.entries(response.timeline)) {
        this.timeline.push({
          time: key,
          // eslint-disable-next-line @typescript-eslint/ban-ts-comment
          // @ts-ignore
          value,
        });
      }

      console.log(response);

      this.chat.push(chatMessage);
    },
    async autoChatMessage(time: number, timestamp: number, callback: any) {
      const m = messages.filter((x) => x.timestamp === time);
      let counter = 0;
      const min = 500;
      const max = 1500;
      // eslint-disable-next-line no-restricted-syntax
      for (const x of m) {
        setTimeout(() => {
          this.sendChatMessage(x.message, timestamp, x.username);
          callback();
        }, counter * Math.random() * (max - min) + min);
        counter += 1;
      }
    },
  },
});
