<template>
  <div class="home h-screen ml-5 mr-5 mt-5">
    <img class="" src="../assets/logo_audiment.png" alt="Logo" width="200" />
    <div
      id="chat"
      class="flex flex-col text-white p-3 rounded-lg font-mono bg-white shadow-lg bg-clip-padding bg-opacity-10 border border-gray-200 backdrop-filter backdrop-blur-xl h-5/6"
    >
      <div class="mb-2">CHAT</div>
      <div id="messages" class="overflow-y-auto text-sm mb-auto h-full overflow-auto">
        <div v-for="message in chat" :key="message.timestamp">
          <span class="text-blue-400">{{ message.username }}&nbsp;</span>
          <span> {{ message.message }}</span>
        </div>
      </div>

      <input
        v-model="nameBox"
        placeholder="Your Name"
        class="mb-2 bottom-0 opacity-20 text-white shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      />
      <input
        v-model="messageBox"
        v-on:keyup.enter="
          sendMessage();
          newChatMessageCallback();
        "
        class="mb-2 bottom-0 opacity-20 text-white shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      />
      <button
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
        @click="
          sendMessage();
          newChatMessageCallback();
        "
        v-if="messageBox !== '' && messageBox.trim() !== ''"
      >
        Send
      </button>
      <button
        class="bg-blue-500 text-white font-bold py-2 px-4 rounded opacity-50 cursor-not-allowed"
        disabled
        v-else
      >
        Send
      </button>
      <!-- <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          @click="
            sendMessage();
            newChatMessageCallback();
          "
          :disabled="messageBox.length === 0"
        >
          Send Chat Message
        </button> -->
    </div>
  </div>
</template>

<script lang="ts">
// eslint-disable-next-line object-curly-newline
import { defineComponent, onMounted, ref, computed } from 'vue';

// eslint-disable-next-line object-curly-newline

import { useChatStore } from '../stores';

// import { WordCloud } from '../components/WordCloud';

export default defineComponent({
  name: 'ChatView',
  components: {},
  data() {
    return {
      videoElement: null,
      time: 0,
      isRunning: false,
      interval: null,
      url: process.env.VUE_APP_API_URL || 'http://localhost:8080',
    };
  },
  methods: {
    newChatMessageCallback() {
      const objDiv = document.getElementById('messages');
      objDiv!.scrollTop = objDiv?.scrollHeight || 0;
    },
  },
  watch: {
    chat: {
      handler(newValue, oldValue) {
        setTimeout(() => {
          this.newChatMessageCallback();
        }, 10);
      },
      deep: true,
    },
  },
  setup() {
    const chatStore = useChatStore();
    chatStore.init();
    chatStore.getChatMessages();
    const loading = ref(true);
    const messageBox = ref('');
    const nameBox = ref('');
    const startTime = ref(0);

    onMounted(async () => {
      loading.value = false;
    });

    const sendMessage = () => {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      chatStore.sendChatMessage(messageBox.value, startTime.value, nameBox.value);
      messageBox.value = '';
    };

    return {
      chat: computed(() => chatStore.getChat),
      loading,
      messageBox,
      nameBox,
      sendMessage,
      startTime,
    };
  },
});
</script>
