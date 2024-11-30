<template>
  <v-container>
    <v-card class="pa-6">
      <!-- Top: L and R Buttons -->
      <v-row justify="space-between" align="center" class="mb-6">
        <v-btn
          outlined
          class="button l-button"
          @click="handleButtonClick('L')"
        >
          L
        </v-btn>
        <v-btn
          outlined
          class="button r-button"
          @click="handleButtonClick('R')"
        >
          R
        </v-btn>
      </v-row>

      <v-row>
        <!-- Left: D-Pad -->
        <v-col cols="1" offset="2">
          <div class="buttons-grid">
            <v-btn
              outlined
              class="button"
              @click="handleButtonClick('Up')"
            >
              Up
            </v-btn>
              <v-btn
                outlined
                class="button"
                @click="handleButtonClick('Left')"
              >
                Left
              </v-btn>
              <v-btn
                outlined
                class="button"
                @click="handleButtonClick('Right')"
              >
                Right
              </v-btn>
            <v-btn
              outlined
              class="button"
              @click="handleButtonClick('Down')"
            >
              Down
            </v-btn>
          </div>
        </v-col>

        <!-- Right: Y, X, A, B Buttons -->
        <v-col cols="1" offset="4">
          <div class="buttons-grid">
            <v-btn
              outlined
              class="button y-button"
              color="yellow darken-2"
              @click="handleButtonClick('Y')"
            >
              Y
            </v-btn>
            <v-btn
              outlined
              class="button x-button"
              color="blue darken-2"
              @click="handleButtonClick('X')"
            >
              X
            </v-btn>
            <v-btn
              outlined
              class="button a-button"
              color="green darken-2"
              @click="handleButtonClick('A')"
            >
              A
            </v-btn>
            <v-btn
              outlined
              class="button b-button"
              color="red darken-2"
              @click="handleButtonClick('B')"
            >
              B
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script setup>
function handleButtonClick(button) {
  console.log(`${button} clicked!`);
  // Add your logic here for each button click
}
</script>

<style scoped>
/* General Styles */
.button {
  width: 64px;
  height: 64px;
  font-weight: bold;
  font-size: 16px;
}

/* D-Pad Styles */
.dpad {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.dpad-middle {
  display: flex;
  justify-content: space-between;
  width: 160px;
  margin: 8px 0;
}

.dpad-button {
  min-width: 64px;
  min-height: 64px;
  font-weight: bold;
}

/* Buttons Grid for Y, X, A, B */
.buttons-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  justify-items: center;
}

/* L and R Buttons */
.l-button,
.r-button {
  width: 80px;
  height: 64px;
  font-weight: bold;
  font-size: 16px;
}
</style>
