import { LocalStorage } from "quasar";
import axios from "axios";

import Router from "../router/index.js";

export const reqInstance = axios.create({
  headers: {
    Authorization: `Bearer ${LocalStorage.getItem("CATGInventoryToken")}`,
  },
});

export const sendRequest = async (config) => {
  try {
    const response = await reqInstance(config);
    return response.data;
  } catch (error) {
    if (error.response.status === 403) {
      //router.push("/login");
    }
    throw error;
  }
};
