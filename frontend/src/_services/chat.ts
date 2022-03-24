import axios from 'axios';
import { Launch } from '@/interfaces/launches';
import { ChatMessage } from '@/interfaces/chat';

export const createChatMessage = async (message: ChatMessage): Promise<boolean> =>
  // eslint-disable-next-line implicit-arrow-linebreak
  axios
    .post('http://localhost:8080/message/', {
      message: message.message,
      timestamp: message.timestamp,
    })
    .then((response) => true)
    .catch((error) => {
      console.log(error);
      return false;
    });

export const test = (): void => {
  console.log();
};
