// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as diff from 'diff';

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



	// ファイルの変更内容を追跡する関数
	function handleActiveEditorChange(editor?: vscode.TextEditor) {
		if (editor) {
			// アクティブなエディタが存在する場合
			console.log('ファイルが開かれました:', editor.document.fileName);
			console.log('言語:', editor.document.languageId);
			// previousContent = editor.document.getText();
			// setInterval(checkForFileDiff, 10 * 1000);
		}
	};

	/*

	let previousContent: string = '';

	// 差分検出用関数
	function checkForFileDiff() {
		const editor = vscode.window.activeTextEditor;
		if (editor) {
			const currentContent = editor.document.getText();
			if (currentContent !== previousContent) {
				// ファイルの差分を計算
				const differences = diff.diffChars(previousContent, currentContent);

				// 差分を表示
				differences.forEach(part => {
					if (part.added) {
						console.log(`追加された行: ${part.value}`);
					}
					if (part.removed) {
						console.log(`削除された行: ${part.value}`);
					}
				});

				// 現在のコンテンツを保存
				previousContent = currentContent;
			}
		}
	}

	*/

	let openedContent: string | null = null;

	function trackOpenedContent(document: vscode.TextDocument) {
		if (document && document.languageId !== 'plaintext') {
			openedContent = document.getText();
		}
	}

	function checkForDiffAndNotify(document: vscode.TextDocument) {
		if (document && openedContent && document.languageId !== 'plaintext') {
			const currentContent = document.getText();
			const differences = diff.diffChars(openedContent, currentContent);

			differences.forEach(part => {
				if (part.added) {
					vscode.window.showInformationMessage(`追加された内容: ${part.value}`);
				}
				if (part.removed) {
					vscode.window.showInformationMessage(`削除された内容: ${part.value}`);
				}
			});
		}
	}


	context.subscriptions.push(
		vscode.window.registerUriHandler({
			handleUri
		}),

		// vscode.window.onDidChangeActiveTextEditor((editor) => {
		// 	handleActiveEditorChange(editor);
		// }),
		vscode.workspace.onDidOpenTextDocument((document) => {
			// ドキュメントが開かれたときの処理
			console.log('ファイルが開かれました:', document.fileName);
			console.log(document.languageId);
		}),

		vscode.workspace.onDidOpenTextDocument((document) => {
			trackOpenedContent(document);
		}),
		vscode.workspace.onDidCloseTextDocument((document) => {
			checkForDiffAndNotify(document);
		}),
		disposable
	);

	// const activeEditor = vscode.window.activeTextEditor;

	// if (activeEditor) {
	// 	const fileName = activeEditor.document.fileName;
	// 	vscode.window.showInformationMessage(`ファイル名: ${fileName}`);
	// } else {
	// 	vscode.window.showInformationMessage('エディタが開いていません');
	// }
}


// This method is called when your extension is deactivated
export function deactivate() { }
