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

type ChatState = {
  chat: ChatMessage[];
  sentiment: Sentiment;
};

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
        overallSentiment: 'string',
        positive: 0,
      },
    }),
  getters: {
    getChat(): ChatMessage[] {
      return this.chat;
    },
    getSentiment(): Sentiment {
      return this.sentiment;
    },
  },
  actions: {
    // any amount of arguments, return a promise or not
    async sendChatMessage(message: string) {
      const chatMessage: ChatMessage = {
        message,
        timestamp: Date.now(),
        username: 'xxGamer2001xx',
      };
      const response = await createChatMessage(chatMessage);
      console.log(response);
      this.sentiment = {
        overallSentiment: response.avg_sentiment.overall_sentiment,
        ...response.avg_sentiment,
      };
      this.chat.push(chatMessage);
    },
  },
});
