<template>
  <div class="home">
    <img class="" src="../assets/logo_audiment.png" alt="Logo" width="200" />
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
          width="250"
          v-if="sentiment.overallSentiment === 'Positive'"
        />
        <img
          class="flex items-center mx-auto mt-10 filter drop-shadow-2xl"
          src="../assets/neutral.png"
          alt="Neutral Avatar"
          width="250"
          v-if="sentiment.overallSentiment === 'Neutral'"
        />
        <img
          class="flex items-center mx-auto mt-10 filter drop-shadow-2xl"
          src="../assets/sad.png"
          alt="Sad Avatar"
          width="250"
          v-if="sentiment.overallSentiment === 'Negative'"
        />
      </div>
      <div
        id="stream"
        class="col-span-6 text-white m-2 p-3 rounded-lg font-mono h-96 bg-white shadow-lg bg-clip-padding bg-opacity-10 border border-gray-200 backdrop-blur-md"
      >
        <div class="mb-2">LIVE</div>
        <video
          class="flex flex-col items-center mx-auto rounded-lg"
          width="550"
          controls
          @playing="startPlaying"
          @pause="updatePaused"
        >
          <source :src="`${url}/video/`" type="video/mp4" />
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
          v-on:keyup.enter="
            sendMessage();
            newChatMessageCallback();
          "
          class="bottom-0 opacity-20 text-white shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
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
    <div class="grid grid-cols-12 gap-1">
      <div
        id="stream"
        class="col-span-7 text-white m-2 p-3 rounded-lg font-mono h-56 bg-white shadow-lg bg-clip-padding bg-opacity-10 border border-gray-200 backdrop-filter backdrop-blur-xl"
      >
        SENTIMENT TRACKER
        <LineChart style="max-height: 100%" v-bind="lineChartProps" />
      </div>
      <!-- <div
        id="stream"
        class="col-span-5 text-white m-2 p-3 rounded-lg font-mono h-56 bg-white shadow-lg bg-clip-padding bg-opacity-10 border border-gray-200 backdrop-filter backdrop-blur-xl"
      >
        <ul class="cloud" role="navigation" aria-label="Webdev word cloud">
          <li v-for="word in wordCloud" :key="word.text">
            <a
              href="#"
              :data-weight="Math.floor(Math.abs(word.value))"
              :style="word.value > 0 ? 'color: green' : 'color: red'"
              >{{ word.text }}</a
            >
          </li>
        </ul>

        {{ wordCloud }}
      </div> -->

      <div
        id="stream"
        class="col-span-5 text-white m-2 p-3 rounded-lg font-mono h-56 bg-white shadow-lg bg-clip-padding bg-opacity-10 border border-gray-200 backdrop-filter backdrop-blur-xl content-center"
      >
      IMPACT CLOUD
        <p
          v-if="wordCloud[0]"
          :style="wordCloud[0].value > 0 ? 'color: #4ade80' : 'color: #ef4444'"
          class="text-xl font-sans"
        >
          {{ wordCloud[0].text }}
        </p>
        <br />
        <p
          v-if="wordCloud[1]"
          :style="wordCloud[1].value > 0 ? 'color: #4ade80' : 'color: #ef4444'"
          class="text-lg font-sans"
        >
          {{ wordCloud[1].text }}
        </p>
        <br />
        <p
          v-if="wordCloud[2]"
          :style="wordCloud[2].value > 0 ? 'color: #4ade80' : 'color: #ef4444'"
          class="text-base font-sans"
        >
          {{ wordCloud[2].text }}
        </p>

        <!-- {{ wordCloud }} -->
      </div>
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

// import { WordCloud } from '../components/WordCloud';

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
      url: process.env.VUE_APP_API_URL || 'http://localhost:8080',
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
      this.autoChatMessage(this.time, this.startTime, this.newChatMessageCallback);
    },
    newChatMessageCallback() {
      this.updateChart();
      const objDiv = document.getElementById('messages');
      objDiv!.scrollTop = objDiv?.scrollHeight || 0;
    },
  },
  setup() {
    const chatStore = useChatStore();
    const loading = ref(true);
    const messageBox = ref('');
    const startTime = ref(0);

    const dataValues = ref([] as number[]);
    const dataValues2 = ref([] as number[]);
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
          borderColor: 'white',
        },
        {
          data: dataValues2.value,
          tension: 0.4,
          borderColor: 'white',
          pointRadius: 0,
          stepped: true,
          borderDash: [5, 5],
          borderWidth: 1,
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
          suggestedMin: -1.0,
          suggestedMax: 1.0,
        },
      },
      elements: {
        point: {
          radius: 0,
        },
      },
      annotation: {
        annotations: [
          {
            type: 'line',
            mode: 'horizontal',
            scaleID: 'y-axis-0',
            value: 0,
            borderColor: '#FFFFFF',
            borderWidth: 4,
          },
        ],
      },
    }));

    const { lineChartProps, lineChartRef } = useLineChart({
      chartData: lineData,
      options,
    });

    const updateChart = () => {
      dataLabels.value = chatStore.getTimeline.map((x) => x.time);
      dataValues.value = chatStore.getTimeline.map((x) => x.value);
      dataValues2.value = chatStore.getTimeline.map((x) => 0);
    };

    return {
      chat: computed(() => chatStore.getChat),
      sentiment: computed(() => chatStore.getSentiment),
      timeline: computed(() => chatStore.getTimeline),
      wordCloud: computed(() => chatStore.getWordCloud),
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

ul.cloud {
  list-style: none;
  padding-left: 0;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  line-height: 2.75rem;
  width: 450px;
}

ul.cloud a {
  /*
  Not supported by any browser at the moment :(
  --size: attr(data-weight number);
  */
  --size: 4;
  --color: #a33;
  color: var(--color);
  font-size: calc(var(--size) * 0.18rem + 0.375rem);
  display: block;
  padding: 0.125rem 0.25rem;
  position: relative;
  text-decoration: none;
  /*
  For different tones of a single color
  opacity: calc((15 - (9 - var(--size))) / 15);
  */
}

ul.cloud a[data-weight='1'] {
  --size: 1;
}
ul.cloud a[data-weight='2'] {
  --size: 2;
}
ul.cloud a[data-weight='3'] {
  --size: 3;
}
ul.cloud a[data-weight='4'] {
  --size: 4;
}
ul.cloud a[data-weight='5'] {
  --size: 6;
}
ul.cloud a[data-weight='6'] {
  --size: 8;
}
ul.cloud a[data-weight='7'] {
  --size: 10;
}
ul.cloud a[data-weight='8'] {
  --size: 13;
}
ul.cloud a[data-weight='9'] {
  --size: 16;
}

ul[data-show-value] a::after {
  content: ' (' attr(data-weight) ')';
  font-size: 1rem;
}

ul.cloud li:nth-child(2n + 1) a {
  --color: #181;
}
ul.cloud li:nth-child(3n + 1) a {
  --color: #33a;
}
ul.cloud li:nth-child(4n + 1) a {
  --color: #c38;
}

ul.cloud a:focus {
  outline: 1px dashed;
}

ul.cloud a::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  width: 0;
  height: 100%;
  background: var(--color);
  transform: translate(-50%, 0);
  opacity: 0.15;
  transition: width 0.25s;
}

/* ul.cloud a:focus::before,
ul.cloud a:hover::before {
  width: 100%;
} */

@media (prefers-reduced-motion) {
  ul.cloud * {
    transition: none !important;
  }
}
</style>
