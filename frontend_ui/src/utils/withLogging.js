import { useLoggerStore } from '@/stores/loggerStore';

/**
 * Logs requests and responses for any API call.
 * @param {string} cmdName - The command name (endpoint path).
 * @param {string} requestMessage - Description of the request being made.
 * @param {function} apiCall - The API call function that returns a promise.
 * @param {boolean} loggerRequired - Whether to log the response.
 * @returns {Promise<any>} - The API response data.
 */
export async function withLogging(cmdName, requestMessage, apiCall, loggerRequired = true) {
  const loggerStore = useLoggerStore();

  // Log the request
  if (loggerRequired)
  loggerStore.addLog(cmdName, requestMessage);

  try {
    const response = await apiCall();

    if (response.data.status === "NOT-OK") throw response.data
    // Log the response
    const responseMessage = `Status: ${response.data.status}, Message: ${response.data.message}`;
    if (loggerRequired)
    loggerStore.addLog(`${cmdName} - response`, responseMessage);

    return response.data;
  } catch (error) {
    // Log the error response
    const errorMessage = `Error: ${error.response?.data?.message || error.message}`;
    if (loggerRequired)
    loggerStore.addLog(`${cmdName} - response`, errorMessage);

    throw error;
  }
}
