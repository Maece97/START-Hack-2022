import axios from 'axios';
import { Launch } from '@/interfaces/launches';

export const getLatestLaunch = async (): Promise<Launch> =>
  // eslint-disable-next-line implicit-arrow-linebreak
  axios
    .get('https://api.spacexdata.com/v4/launches/latest')
    .then((response) => response.data)
    .catch((error) => {
      console.log(error);
      return undefined;
    });

export const test = (): void => {
  console.log();
};
