import { defineStore } from 'pinia';
import { ChatMessage } from '@/interfaces/chat';
import { createChatMessage } from '@/_services/chat';

type ChatState = {
  chat: ChatMessage[];
};

// eslint-disable-next-line import/prefer-default-export
export const useChatStore = defineStore('chat', {
  state: (): ChatState =>
    // eslint-disable-next-line implicit-arrow-linebreak
    ({
      chat: [],
    }),
  getters: {
    getChat(): ChatMessage[] {
      return this.chat;
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
      if (await createChatMessage(chatMessage)) {
        this.chat.push(chatMessage);
      }
    },
  },
});
