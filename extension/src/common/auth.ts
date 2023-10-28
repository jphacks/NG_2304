import { ExtensionContext, SecretStorage } from "vscode";
import axios from "axios";

export default class AuthSettings {
    private static _instance: AuthSettings;

    constructor(private secretStorage: SecretStorage) {}

    static init(context: ExtensionContext): void {
        /*
        Create instance of new AuthSettings.
        */
        AuthSettings._instance = new AuthSettings(context.secrets);
    }

    static get instance(): AuthSettings {
        /*
        Getter of our AuthSettings existing instance.
        */
        return AuthSettings._instance;
    }

    async storeAuthData(key: string, token?: string): Promise<void> {
        /*
        Update values in bugout_auth secret storage.
        */
        if (token) {
            this.secretStorage.store(key, token);
        }
    }

    async getAuthData(key: string): Promise<string | undefined> {
        /*
        Retrieve data from secret storage.
        */
        return await this.secretStorage.get(key);
    }
}

// export async function genToken(seal: string) {
//     //POSTリクエスト（通信）
//     const data = { seal };
//     const url = await axios.post("http://localhost:3000/api/token", data)

//             .then((url) => {
//                 // console.log(url);
//                 return url["data"];
//             })

//             .catch(err => {
//             console.log("err:", err);
//             });
//     // return "session_id";
// }

export async function genToken(seal: string) {
    // POSTリクエスト（通信）
    const data = { seal };
    try {
        const response = await axios.post("http://localhost:3000/api/token", data);
        const responseDataAsString = JSON.parse(JSON.stringify(response.data)); // レスポンスデータを文字列に変換
        return responseDataAsString;
    } catch (err) {
        console.log("err:", err);
        // エラーが発生した場合、エラー処理を行ったり、適切な値を返したりできます。
        // この例では、エラーの場合はnullを返しますが、適切なエラーハンドリングを行ってください。
        return null;
    }
}


