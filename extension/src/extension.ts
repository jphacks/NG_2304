// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

import { githublogin } from './common/login';
import { githubLoginUri } from './static';
import AuthSettings from './common/auth';
import { genToken } from './common/auth';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "extension" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('extension.githubLogin', () => {

		vscode.window.showInformationMessage('Github Login Command');

		githublogin(githubLoginUri);
	});


	/// おやすみ now(2023/10/28 01:58 起きるまで3時間ない)
	const handleUri = async (uri: vscode.Uri) => {
		const queryParams = new URLSearchParams(uri.query);

		if (queryParams.has('seal')) {

			// console.log(`${queryParams.get('seal') as string}`);

			let token = await genToken(`${queryParams.get('seal') as string}`);

			// console.log(token);
			// console.log(token['session_id']);

			AuthSettings.init(context);
			const settings = AuthSettings.instance;

			// session_id, access_tokenをSecretStorageに格納
			settings.storeAuthData("session_id", token['session_id']);
			settings.storeAuthData("access_token", token['access_token']);

			// session_id, access_token呼び出しテスト
			const tokenOutput = await settings.getAuthData("session_id");
			const tokenOutput2 = await settings.getAuthData("access_token");
			console.log("せっしょんid" + tokenOutput);
			console.log("あくせすとーくん" + tokenOutput2);
		}
	};

	context.subscriptions.push(
		vscode.window.registerUriHandler({
			handleUri
		}),
		disposable
	);
}


// This method is called when your extension is deactivated
export function deactivate() { }
