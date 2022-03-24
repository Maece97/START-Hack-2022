<template>
  <div class="home">
    <div class="grid grid-cols-12 gap-1">
      <div id="avatar" class="col-span-3">Avatar</div>
      <div id="stream" class="col-span-6">Stream</div>
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
    return {};
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
