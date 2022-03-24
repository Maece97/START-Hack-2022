<template>
  <div class="home">
    <div id="chat">
      {{ chat }}
      <button @click="createMessage('Hello')">Send Chat Message</button>
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
  setup() {
    const chatStore = useChatStore();
    const loading = ref(true);

    onMounted(async () => {
      loading.value = false;
    });

    return {
      chat: computed(() => chatStore.getChat),
      loading,
      createMessage: (message: string) => chatStore.sendChatMessage(message),
    };
  },
});
</script>
