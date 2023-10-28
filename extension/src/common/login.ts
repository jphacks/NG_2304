import * as vscode from 'vscode';

export function githublogin(githubLoginUri: string) {
    vscode.env.openExternal(vscode.Uri.parse(githubLoginUri));
}