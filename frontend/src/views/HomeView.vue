<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
    Test {{ launch.rocket }}
    <hr />
    {{ launch }}
  </div>
</template>

<script lang="ts">
// eslint-disable-next-line object-curly-newline
import { defineComponent, onMounted, ref, computed } from 'vue';
import HelloWorld from '../components/HelloWorld.vue'; // @ is an alias to /src

import { useLaunchesStore } from '../stores';

export default defineComponent({
  name: 'HomeView',
  components: {
    HelloWorld,
  },
  setup() {
    const launchesStore = useLaunchesStore();
    const loading = ref(true);

    onMounted(async () => {
      await launchesStore.loadLaunches();
      loading.value = false;
      console.log('ttt', launchesStore.latestLaunch);
    });

    return {
      launch: computed(() => launchesStore.latestLaunchT),
      loading,
    };
  },
});
</script>
