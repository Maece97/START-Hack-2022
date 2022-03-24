import axios from 'axios';
import { Launch } from '@/interfaces/launches';
import { ChatMessage } from '@/interfaces/chat';

export const createChatMessage = async (message: ChatMessage): Promise<any> =>
  // eslint-disable-next-line implicit-arrow-linebreak
  axios
    .post('http://localhost:8080/message/', {
      message: message.message,
      timestamp: message.timestamp,
      username: message.username,
      startTime: message.startTime,
    })
    .then((response) => response.data)
    .catch((error) => {
      console.log(error);
      return false;
    });

export const test = (): void => {
  console.log({
    message: 'MEssage heyhey',
    timestamp: 1234556677,
    username: 'proGamerLPHD',
  });
};
