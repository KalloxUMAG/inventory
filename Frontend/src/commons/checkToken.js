import { LocalStorage } from 'quasar';
import axios from 'axios';

export const checkToken = async() => {
    const api_prefix = process.env.API_URL;
    const key = "CATGInventoryToken"
    let value = {access_token: LocalStorage.getItem(key), token_type: "nowonder"}
    try {
        const response = await axios.get(api_prefix + "/users/me/", value);
        return response;
    } catch (error) {
    }
}


