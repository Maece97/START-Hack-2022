<template>
  <div class="home">
    <div class="grid grid-cols-12 gap-1">
      <div id="avatar" class="col-span-3">Avatar<br />{{ sentiment }}</div>
      <div id="stream" class="col-span-6">
        <video width="320" height="240" controls @playing="startPlaying" @pause="updatePaused">
          <source src="http://localhost:8080/video/" type="video/mp4" />
          <track kind="captions" />
          Your browser does not support the video tag.
        </video>
        {{ time }}
      </div>
      <div id="chat" class="col-span-3">
        <div v-for="message in chat" :key="message.timestamp">
          <span class="text-blue-400">{{ message.username }}&nbsp;</span>
          <span> {{ message.message }}</span>
        </div>
        <input
          v-model="messageBox"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          @click="sendMessage()"
          :disabled="messageBox.length === 0"
        >
          Send Chat Message
        </button>
      </div>
    </div>
    <div class="grid grid-cols-12 gap-1">
      <div id="stream" class="col-span-7">Line thingy</div>
      <div id="stream" class="col-span-5"></div>
    </div>
  </div>
</template>

<script lang="ts">
// eslint-disable-next-line object-curly-newline
import { defineComponent, onMounted, ref, computed } from 'vue';

import { useChatStore } from '../stores';

export default defineComponent({
  name: 'HomeView',
  components: {},
  data() {
    return {
      videoElement: null,
      time: 0,
      isRunning: false,
      interval: null,
    };
  },
  methods: {
    startPlaying(event: any) {
      console.log('test1');
      this.videoElement = event.target;
      this.toggleTimer();
    },
    updatePaused(event: any) {
      this.toggleTimer();
    },
    toggleTimer() {
      if (this.isRunning) {
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        clearInterval(this.interval);
        console.log('timer stops');
      } else {
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        this.interval = setInterval(this.incrementTime, 1000);
      }
      this.isRunning = !this.isRunning;
    },
    incrementTime() {
      this.time += 1;
    },
  },
  setup() {
    const chatStore = useChatStore();
    const loading = ref(true);
    const messageBox = ref('');

    onMounted(async () => {
      loading.value = false;
    });

    const sendMessage = () => {
      chatStore.sendChatMessage(messageBox.value);
      messageBox.value = '';
    };

    return {
      chat: computed(() => chatStore.getChat),
      sentiment: computed(() => chatStore.getSentiment),
      loading,
      messageBox,
      sendMessage,
    };
  },
});
</script>

<style scoped>
#avatar {
  border: solid 1px black;
}
#stream {
  border: solid 1px black;
}
#chat {
  border: solid 1px black;
}
</style>
