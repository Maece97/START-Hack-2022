import { defineStore } from 'pinia';
import { Launch } from '@/interfaces/launches';
import { getLatestLaunch } from '../_services';

type LaunchState = {
  latestLaunch: Launch;
  test: string;
};

// eslint-disable-next-line import/prefer-default-export
export const useLaunchesStore = defineStore('launches', {
  state: (): LaunchState =>
    // eslint-disable-next-line implicit-arrow-linebreak
    ({
      latestLaunch: {
        rocket: '',
      },
      test: '',
    }),
  getters: {
    latestLaunchT(): Launch {
      return this.latestLaunch;
    },
  },
  actions: {
    // any amount of arguments, return a promise or not
    async loadLaunches() {
      const test = await getLatestLaunch();
      console.log('t', test);
      // this.$state = { ...this.$state, latestLaunch: { rocket: test.rocket } };
      // this.latestLaunch = { rocket: test.rocket };
      this.$patch({ latestLaunch: test, test: 'test' });
      // this.test = 'HELLO WORLD';
      // // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // // @ts-ignore
      // this.test = { hello: 'world' };
      // // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // // @ts-ignore
      // // this.$patch = { latestLaunch: { rocket: 'world' } };
      // this.$state.latestLaunch = { rocket: 'world' };
      console.log('test', this.test, this.latestLaunchT);
    },
  },
});
