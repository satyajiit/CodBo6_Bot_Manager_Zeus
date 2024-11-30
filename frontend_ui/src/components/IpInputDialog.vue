<template>
  <v-dialog :model-value="ipDialogVisible" @update:model-value="updateDialog" max-width="600px">
    <v-card>
      <v-card-title class="text-h6">Enter Server IP Addresses</v-card-title>

      <v-card-text>
        <v-form ref="form">
          <v-container>
            <v-row v-for="(ip, index) in ipFields" :key="index" align="center">
              <v-col cols="10">
                <v-text-field
                  v-model="ipFields[index]"
                  label="Server IP Address"
                  placeholder="e.g., 192.168.1.1"
                  :rules="[ipValidationRule]"
                  outlined
                  dense
                />
              </v-col>
              <v-col cols="2" class="text-right">
                <v-btn icon @click="removeField(index)" v-if="ipFields.length > 1">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>

            <v-btn color="primary" text @click="addField">
              Add More IP
            </v-btn>
          </v-container>
        </v-form>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="red" variant="text" @click="closeDialog">Cancel</v-btn>
        <v-btn color="green" variant="text" @click="saveIpAddresses">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, defineEmits, defineProps } from "vue";

// Props for managing the dialog state
defineProps({
  ipDialogVisible: {
    type: Boolean,
    required: true,
  },
});

// Emit events to communicate with the parent
const emit = defineEmits(["update:ipDialogVisible", "save"]);

const ipFields = ref([""]); // Array of IP fields, starts with one empty field
const form = ref(null); // Form reference

// IP address validation rule
const ipValidationRule = (value) => {
  const ipRegex = /^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$/;
  return ipRegex.test(value) || "Invalid IP address";
};

// Function to add a new IP field
const addField = () => {
  ipFields.value.push("");
};

// Function to remove an IP field
const removeField = (index) => {
  ipFields.value.splice(index, 1);
};

// Function to close the dialog
const closeDialog = () => {
  emit("update:ipDialogVisible", false); // Notify parent to close dialog
};

// Function to validate and save the IP addresses
const saveIpAddresses = () => {
  if (form.value?.validate()) {
    const validIps = ipFields.value.filter((ip) => ip.trim() !== "");
    emit("save", validIps); // Emit the valid IPs back to the parent
    emit("update:ipDialogVisible", false); // Close dialog after saving
  }
};

// Function to update the dialog visibility state
const updateDialog = (value) => {
  emit("update:ipDialogVisible", value);
};
</script>

<style scoped>
/* Add any additional styles if needed */
</style>
