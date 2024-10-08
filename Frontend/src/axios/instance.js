import { Cookies } from "quasar";
import axios from "axios";

export const reqInstance = axios.create({
  headers: {
    Authorization: `Bearer ${Cookies.get("CATGInventoryToken")}`,
  },
});

export const sendRequest = async (config) => {
  try {
    const response = await reqInstance(config);
    return response;
  } catch (error) {
    if (error.response.status === 401) {
      Cookies.remove("CATGInventoryToken");
      Cookies.remove("CATGInventoryFullname");
    }
    throw error;
  }
};
