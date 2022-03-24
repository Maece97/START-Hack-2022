<template>
  <div class="home">
        <img
          class=""
          src="../assets/logo_audiment.png"
          alt="Logo"
          width="200"
        >
      <div class="grid grid-cols-12 gap-1">
      <div
        id="avatar"
        class="col-span-3 text-white m-2 p-3 rounded-lg font-mono h-96 bg-white shadow-lg bg-clip-padding bg-opacity-10 border border-gray-200 backdrop-filter backdrop-blur-xl"
        style="backdrop-filter: blur(20px)"
      >
        AUDITAR<br /><!--{{ sentiment }}-->
        <img
          class="flex items-center mx-auto mt-10 filter drop-shadow-2xl"
          src="../assets/happy.png"
          alt="Happy Avatar"
          width="200"
        />
      </div>
      <div
        id="stream"
        class="col-span-6 text-white m-2 p-3 rounded-lg font-mono h-96 bg-white shadow-lg bg-clip-padding bg-opacity-10 border border-gray-200 backdrop-blur-md"
      >
        <div class="mb-2">KRISTOFERS STREAM</div>
        <video
          class="flex flex-col items-center mx-auto rounded-lg"
          width="550"
          controls
          @playing="startPlaying"
          @pause="updatePaused"
        >
          <source src="http://localhost:8080/video/" type="video/mp4" />
          <track kind="captions" />
          Your browser does not support the video tag.
        </video>
      </div>
      <div
        id="chat"
        class="flex flex-col col-span-3 text-white m-2 p-3 rounded-lg font-mono h-96 bg-white shadow-lg bg-clip-padding bg-opacity-10 border border-gray-200 backdrop-filter backdrop-blur-xl"
      >
      <div class="mb-2">CHAT</div>
      <div id="messages" class="overflow-y-auto text-sm mb-auto h-72 overflow-auto">
        <div v-for="message in chat" :key="message.timestamp">
          <span class="text-blue-400">{{ message.username }}&nbsp;</span>
          <span> {{ message.message }}</span>
        </div>
              </div>

        <input
          v-model="messageBox"
          class="bottom-0 opacity-20 text-white shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
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
      <div
        id="stream"
        class="col-span-7 text-white m-2 p-3 rounded-lg font-mono h-56 bg-white shadow-lg bg-clip-padding bg-opacity-10 border border-gray-200 backdrop-filter backdrop-blur-xl"
      >
        <LineChart v-bind="lineChartProps" />
        {{ timeline }}
        {{ lineChartProps }}
      </div>
      <div
        id="stream"
        class="col-span-5 text-white m-2 p-3 rounded-lg font-mono h-56 bg-white shadow-lg bg-clip-padding bg-opacity-10 border border-gray-200 backdrop-filter backdrop-blur-xl"
      ></div>
    </div>
  </div>
</template>

<script lang="ts">
// eslint-disable-next-line object-curly-newline
import { defineComponent, onMounted, ref, computed } from 'vue';

import { LineChart, useLineChart } from 'vue-chart-3';
// eslint-disable-next-line object-curly-newline
import { Chart, registerables, ChartData, ChartOptions } from 'chart.js';

import { useChatStore } from '../stores';

Chart.register(...registerables);

export default defineComponent({
  name: 'HomeView',
  components: {
    LineChart,
  },
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
      this.videoElement = event.target;
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      this.startTime = Date.now();
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
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      this.autoChatMessage(this.time, this.startTime);
      this.updateChart();
    },
  },
  setup() {
    const chatStore = useChatStore();
    const loading = ref(true);
    const messageBox = ref('');
    const startTime = ref(0);

    const dataValues = ref([] as number[]);
    const dataLabels = ref([] as string[]);

    onMounted(async () => {
      loading.value = false;
    });

    const sendMessage = () => {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      chatStore.sendChatMessage(messageBox.value, startTime.value);
      messageBox.value = '';
    };

    const lineData = computed<ChartData<'line'>>(() => ({
      labels: dataLabels.value,
      datasets: [
        {
          data: dataValues.value,
          tension: 0.4,
          borderColor: '#FF0000',
        },
      ],
    }));

    const options = computed<ChartOptions<'line'>>(() => ({
      plugins: {
        legend: {
          display: false,
        },
      },
      legend: {
        display: false,
      },
      scales: {
        x: {
          display: false,
          title: {
            display: false,
          },
        },
        y: {
          display: false,
          title: {
            display: false,
            text: 'Value',
          },
          suggestedMin: -1.5,
          suggestedMax: 1.5,
        },
      },
    }));

    const { lineChartProps, lineChartRef } = useLineChart({
      chartData: lineData,
      options,
    });

    const updateChart = () => {
      dataLabels.value = chatStore.getTimeline.map((x) => x.time);
      dataValues.value = chatStore.getTimeline.map((x) => x.value);
    };

    return {
      chat: computed(() => chatStore.getChat),
      sentiment: computed(() => chatStore.getSentiment),
      timeline: computed(() => chatStore.getTimeline),
      loading,
      messageBox,
      sendMessage,
      lineChartProps,
      autoChatMessage: chatStore.autoChatMessage,
      lineChartRef,
      startTime,
      updateChart,
    };
  },
});
</script>

<style scoped>
#avatar {
  border: solid 1px white;
}
#stream {
  border: solid 1px white;
}
#chat {
  border: solid 1px white;
}
</style>
