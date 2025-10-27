# External Repository Trigger

This workflow is triggered when an external repository sends a `repository_dispatch` event.

## How it works

The workflow uses GitHub's `repository_dispatch` event type, which allows external repositories or services to trigger workflows via the GitHub API.

## Triggering the workflow from an external repository

To trigger this workflow from an external repository, you need to send a POST request to the GitHub API:

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/ianscrivener/drawthings-community-models-extract/dispatches \
  -d '{"event_type":"external-repo-updated","client_payload":{"repository":"owner/repo","ref":"main"}}'
```

### Required permissions

The Personal Access Token (PAT) used must have the `repo` scope (or `public_repo` for public repositories).

## Triggering from another GitHub Action

You can trigger this workflow from another repository's GitHub Action using the following step:

```yaml
- name: Trigger external repository workflow
  run: |
    curl -X POST \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer ${{ secrets.DISPATCH_TOKEN }}" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      https://api.github.com/repos/ianscrivener/drawthings-community-models-extract/dispatches \
      -d '{"event_type":"external-repo-updated","client_payload":{"repository":"${{ github.repository }}","ref":"${{ github.ref }}","sha":"${{ github.sha }}"}}'
```

Or use the `peter-evans/repository-dispatch` action:

```yaml
- name: Repository Dispatch
  uses: peter-evans/repository-dispatch@v2
  with:
    token: ${{ secrets.DISPATCH_TOKEN }}
    repository: ianscrivener/drawthings-community-models-extract
    event-type: external-repo-updated
    client-payload: '{"repository": "${{ github.repository }}", "ref": "${{ github.ref }}"}'
```

## Event types

The workflow listens for the `external-repo-updated` event type. You can add more event types by modifying the workflow file:

```yaml
on:
  repository_dispatch:
    types: [external-repo-updated, another-event-type]
```

## Client payload

The `client_payload` field in the dispatch request can contain any JSON data you want to pass to the workflow. This data is accessible via `${{ github.event.client_payload }}` in the workflow.

Example payload:
```json
{
  "repository": "owner/repo",
  "ref": "main",
  "sha": "abc123",
  "custom_field": "custom_value"
}
```
