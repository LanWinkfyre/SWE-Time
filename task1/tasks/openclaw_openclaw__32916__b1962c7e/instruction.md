# Locate the commit that introduced this regression

A regression was reported against `openclaw/openclaw`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[Bug]: 2026.3.2 + Llama.cpp with Qwen3.5-A35-A3B

### Bug type

Regression (worked before, now fails)

### Summary

after updating to 2026.3.2 llama.cpp show errors in logs and i recieve 
Invalid diff: now finding less tool calls!" in telegram after every message. , 2026.3.1 works fine:

```
parse: error parsing grammar: number of repetitions exceeds sane defaults, please reduce the number of repetitions
array ::= "[" space ( value ("," space value)* )? "]" space
boolean ::= ("true" | "false") space
char ::= [^"\\\x7F\x00-\x1F] | [\\] (["\\bfnrt] | "u" [0-9a-fA-F]{4})
decimal-part ::= [0-9]{1,16}
integral-part ::= [0] | [1-9] [0-9]{0,15}
json-array ::= "[" space ("]" | json-value ("," space json-value)* space "]") space
json-bool ::= ("true" | "false") space
json-null ::= "null" space
json-number ::= "-"? ("0" | [1-9] [0-9]*) ("." [0-9]+)? (("e" | "E") [+-]? [0-9]+)? space
json-object ::= "{" space ("}" | json-string space ":" space json-value (space "," space json-string space ":" space json-value)* space "}") space
json-string ::= "\"" ( [^"\\] | "\\" ( ["\\/ bfnrt] | "u" [0-9a-fA-F]{4} ) )* "\"" space
json-value ::= json-object | json-array | json-string | json-number | json-bool | json-null
null ::= "null" space
number ::= ("-"? integral-part) ("." decimal-part)? ([eE] [-+]? integral-part)? space
object ::= "{" space ( string ":" space value ("," space string ":" space value)* )? "}" space
root ::= tool-call-root
space ::= | " " | "\n"{1,2} [ \t]{0,20}
string ::= "\"" char* "\"" space
tool-agents-list ::= "<function=" "agents_list" ">\n" "</function>\n"
tool-call ::= "<tool_call>\n" (tool-read | tool-edit | tool-write | tool-exec | tool-process | tool-message | tool-agents-list | tool-sessions-list | tool-sessions-history | tool-sessions-send | tool-sessions-spawn | tool-subagents | tool-session-status | tool-web-fetch | tool-web-search-searxng) "</tool_call>" space
tool-call-root ::= tool-call?
tool-edit ::= "<function=" "edit" ">\n" tool-edit-arg-path? tool-edit-arg-oldText? tool-edit-arg-newText? tool-edit-arg-file-path? tool-edit-arg-old-string? tool-edit-arg-new-string? "</function>\n"
tool-edit-arg-file-path ::= "<parameter=" "file_path" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-edit-arg-new-string ::= "<parameter=" "new_string" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-edit-arg-newText ::= "<parameter=" "newText" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-edit-arg-old-string ::= "<parameter=" "old_string" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-edit-arg-oldText ::= "<parameter=" "oldText" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-edit-arg-path ::= "<parameter=" "path" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-exec ::= "<function=" "exec" ">\n" tool-exec-arg-command tool-exec-arg-workdir? tool-exec-arg-env? tool-exec-arg-yieldMs? tool-exec-arg-background? tool-exec-arg-timeout? tool-exec-arg-pty? tool-exec-arg-elevated? tool-exec-arg-host? tool-exec-arg-security? tool-exec-arg-ask? tool-exec-arg-node? "</function>\n"
tool-exec-arg-ask ::= "<parameter=" "ask" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-exec-arg-background ::= "<parameter=" "background" ">\n" boolean "</parameter>\n"?
tool-exec-arg-command ::= "<parameter=" "command" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-exec-arg-elevated ::= "<parameter=" "elevated" ">\n" boolean "</parameter>\n"?
tool-exec-arg-env ::= "<parameter=" "env" ">\n" tool-exec-arg-env-schema "</parameter>\n"?
tool-exec-arg-env-schema ::= object
tool-exec-arg-host ::= "<parameter=" "host" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-exec-arg-node ::= "<parameter=" "node" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-exec-arg-pty ::= "<parameter=" "pty" ">\n" boolean "</parameter>\n"?
tool-exec-arg-security ::= "<parameter=" "security" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-exec-arg-timeout ::= "<parameter=" "timeout" ">\n" number "</parameter>\n"?
tool-exec-arg-workdir ::= "<parameter=" "workdir" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-exec-arg-yieldMs ::= "<parameter=" "yieldMs" ">\n" number "</parameter>\n"?
tool-message ::= "<function=" "message" ">\n" tool-message-arg-action tool-message-arg-channel? tool-message-arg-target? tool-message-arg-targets? tool-message-arg-accountId? tool-message-arg-dryRun? tool-message-arg-message? tool-message-arg-effectId? tool-message-arg-effect? tool-message-arg-media? tool-message-arg-filename? tool-message-arg-buffer? tool-message-arg-contentType? tool-message-arg-mimeType? tool-message-arg-caption? tool-message-arg-path? tool-message-arg-filePath? tool-message-arg-replyTo? tool-message-arg-threadId? tool-message-arg-asVoice? tool-message-arg-silent? tool-message-arg-quoteText? tool-message-arg-bestEffort? tool-message-arg-gifPlayback? tool-message-arg-messageId? tool-message-arg-message-id? tool-message-arg-emoji? tool-message-arg-remove? tool-message-arg-targetAuthor? tool-message-arg-targetAuthorUuid? tool-message-arg-groupId? tool-message-arg-limit? tool-message-arg-before? tool-message-arg-after? tool-message-arg-around? tool-message-arg-fromMe? tool-message-arg-includeArchived? tool-message-arg-pollQuestion? tool-message-arg-pollOption? tool-message-arg-pollDurationHours? tool-message-arg-pollMulti? tool-message-arg-channelId? tool-message-arg-channelIds? tool-message-arg-guildId? tool-message-arg-userId? tool-message-arg-authorId? tool-message-arg-authorIds? tool-message-arg-roleId? tool-message-arg-roleIds? tool-message-arg-participant? tool-message-arg-emojiName? tool-message-arg-stickerId? tool-message-arg-stickerName? tool-message-arg-stickerDesc? tool-message-arg-stickerTags? tool-message-arg-threadName? tool-message-arg-autoArchiveMin? tool-message-arg-appliedTags? tool-message-arg-query? tool-message-arg-eventName? tool-message-arg-eventType? tool-message-arg-startTime? tool-message-arg-endTime? tool-message-arg-desc? tool-message-arg-location? tool-message-arg-durationMin? tool-message-arg-until? tool-message-arg-reason? tool-message-arg-deleteDays? tool-message-arg-gatewayUrl? tool-message-arg-gatewayToken? tool-message-arg-timeoutMs? tool-message-arg-name? tool-message-arg-type? tool-message-arg-parentId? tool-message-arg-topic? tool-message-arg-position? tool-message-arg-nsfw? tool-message-arg-rateLimitPerUser? tool-message-arg-categoryId? tool-message-arg-clearParent? tool-message-arg-activityType? tool-message-arg-activityName? tool-message-arg-activityUrl? tool-message-arg-activityState? tool-message-arg-status? "</function>\n"
tool-message-arg-accountId ::= "<parameter=" "accountId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-action ::= "<parameter=" "action" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-activityName ::= "<parameter=" "activityName" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-activityState ::= "<parameter=" "activityState" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-activityType ::= "<parameter=" "activityType" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-activityUrl ::= "<parameter=" "activityUrl" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-after ::= "<parameter=" "after" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-appliedTags ::= "<parameter=" "appliedTags" ">\n" tool-message-arg-appliedTags-schema "</parameter>\n"?
tool-message-arg-appliedTags-schema ::= "[" space (string ("," space string)*)? "]" space
tool-message-arg-around ::= "<parameter=" "around" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-asVoice ::= "<parameter=" "asVoice" ">\n" boolean "</parameter>\n"?
tool-message-arg-authorId ::= "<parameter=" "authorId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-authorIds ::= "<parameter=" "authorIds" ">\n" tool-message-arg-authorIds-schema "</parameter>\n"?
tool-message-arg-authorIds-schema ::= "[" space (string ("," space string)*)? "]" space
tool-message-arg-autoArchiveMin ::= "<parameter=" "autoArchiveMin" ">\n" number "</parameter>\n"?
tool-message-arg-before ::= "<parameter=" "before" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-bestEffort ::= "<parameter=" "bestEffort" ">\n" boolean "</parameter>\n"?
tool-message-arg-buffer ::= "<parameter=" "buffer" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-caption ::= "<parameter=" "caption" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-categoryId ::= "<parameter=" "categoryId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-channel ::= "<parameter=" "channel" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-channelId ::= "<parameter=" "channelId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-channelIds ::= "<parameter=" "channelIds" ">\n" tool-message-arg-channelIds-schema "</parameter>\n"?
tool-message-arg-channelIds-schema ::= "[" space (string ("," space string)*)? "]" space
tool-message-arg-clearParent ::= "<parameter=" "clearParent" ">\n" boolean "</parameter>\n"?
tool-message-arg-contentType ::= "<parameter=" "contentType" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-deleteDays ::= "<parameter=" "deleteDays" ">\n" number "</parameter>\n"?
tool-message-arg-desc ::= "<parameter=" "desc" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-dryRun ::= "<parameter=" "dryRun" ">\n" boolean "</parameter>\n"?
tool-message-arg-durationMin ::= "<parameter=" "durationMin" ">\n" number "</parameter>\n"?
tool-message-arg-effect ::= "<parameter=" "effect" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-effectId ::= "<parameter=" "effectId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-emoji ::= "<parameter=" "emoji" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-emojiName ::= "<parameter=" "emojiName" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-endTime ::= "<parameter=" "endTime" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-eventName ::= "<parameter=" "eventName" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-eventType ::= "<parameter=" "eventType" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-filePath ::= "<parameter=" "filePath" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-filename ::= "<parameter=" "filename" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-fromMe ::= "<parameter=" "fromMe" ">\n" boolean "</parameter>\n"?
tool-message-arg-gatewayToken ::= "<parameter=" "gatewayToken" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-gatewayUrl ::= "<parameter=" "gatewayUrl" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-gifPlayback ::= "<parameter=" "gifPlayback" ">\n" boolean "</parameter>\n"?
tool-message-arg-groupId ::= "<parameter=" "groupId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-guildId ::= "<parameter=" "guildId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-includeArchived ::= "<parameter=" "includeArchived" ">\n" boolean "</parameter>\n"?
tool-message-arg-limit ::= "<parameter=" "limit" ">\n" number "</parameter>\n"?
tool-message-arg-location ::= "<parameter=" "location" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-media ::= "<parameter=" "media" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-message ::= "<parameter=" "message" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-message-id ::= "<parameter=" "message_id" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-messageId ::= "<parameter=" "messageId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-mimeType ::= "<parameter=" "mimeType" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-name ::= "<parameter=" "name" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-nsfw ::= "<parameter=" "nsfw" ">\n" boolean "</parameter>\n"?
tool-message-arg-parentId ::= "<parameter=" "parentId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-participant ::= "<parameter=" "participant" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-path ::= "<parameter=" "path" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-pollDurationHours ::= "<parameter=" "pollDurationHours" ">\n" number "</parameter>\n"?
tool-message-arg-pollMulti ::= "<parameter=" "pollMulti" ">\n" boolean "</parameter>\n"?
tool-message-arg-pollOption ::= "<parameter=" "pollOption" ">\n" tool-message-arg-pollOption-schema "</parameter>\n"?
tool-message-arg-pollOption-schema ::= "[" space (string ("," space string)*)? "]" space
tool-message-arg-pollQuestion ::= "<parameter=" "pollQuestion" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-position ::= "<parameter=" "position" ">\n" number "</parameter>\n"?
tool-message-arg-query ::= "<parameter=" "query" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-quoteText ::= "<parameter=" "quoteText" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-rateLimitPerUser ::= "<parameter=" "rateLimitPerUser" ">\n" number "</parameter>\n"?
tool-message-arg-reason ::= "<parameter=" "reason" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-remove ::= "<parameter=" "remove" ">\n" boolean "</parameter>\n"?
tool-message-arg-replyTo ::= "<parameter=" "replyTo" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-roleId ::= "<parameter=" "roleId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-roleIds ::= "<parameter=" "roleIds" ">\n" tool-message-arg-roleIds-schema "</parameter>\n"?
tool-message-arg-roleIds-schema ::= "[" space (string ("," space string)*)? "]" space
tool-message-arg-silent ::= "<parameter=" "silent" ">\n" boolean "</parameter>\n"?
tool-message-arg-startTime ::= "<parameter=" "startTime" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-status ::= "<parameter=" "status" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-stickerDesc ::= "<parameter=" "stickerDesc" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-stickerId ::= "<parameter=" "stickerId" ">\n" tool-message-arg-stickerId-schema "</parameter>\n"?
tool-message-arg-stickerId-schema ::= "[" space (string ("," space string)*)? "]" space
tool-message-arg-stickerName ::= "<parameter=" "stickerName" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-stickerTags ::= "<parameter=" "stickerTags" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-target ::= "<parameter=" "target" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-targetAuthor ::= "<parameter=" "targetAuthor" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-targetAuthorUuid ::= "<parameter=" "targetAuthorUuid" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-targets ::= "<parameter=" "targets" ">\n" tool-message-arg-targets-schema "</parameter>\n"?
tool-message-arg-targets-schema ::= "[" space (string ("," space string)*)? "]" space
tool-message-arg-threadId ::= "<parameter=" "threadId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-threadName ::= "<parameter=" "threadName" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-timeoutMs ::= "<parameter=" "timeoutMs" ">\n" number "</parameter>\n"?
tool-message-arg-topic ::= "<parameter=" "topic" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-type ::= "<parameter=" "type" ">\n" number "</parameter>\n"?
tool-message-arg-until ::= "<parameter=" "until" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-message-arg-userId ::= "<parameter=" "userId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-process ::= "<function=" "process" ">\n" tool-process-arg-action tool-process-arg-sessionId? tool-process-arg-data? tool-process-arg-keys? tool-process-arg-hex? tool-process-arg-literal? tool-process-arg-text? tool-process-arg-bracketed? tool-process-arg-eof? tool-process-arg-offset? tool-process-arg-limit? tool-process-arg-timeout? "</function>\n"
tool-process-arg-action ::= "<parameter=" "action" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-process-arg-bracketed ::= "<parameter=" "bracketed" ">\n" boolean "</parameter>\n"?
tool-process-arg-data ::= "<parameter=" "data" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-process-arg-eof ::= "<parameter=" "eof" ">\n" boolean "</parameter>\n"?
tool-process-arg-hex ::= "<parameter=" "hex" ">\n" tool-process-arg-hex-schema "</parameter>\n"?
tool-process-arg-hex-schema ::= "[" space (string ("," space string)*)? "]" space
tool-process-arg-keys ::= "<parameter=" "keys" ">\n" tool-process-arg-keys-schema "</parameter>\n"?
tool-process-arg-keys-schema ::= "[" space (string ("," space string)*)? "]" space
tool-process-arg-limit ::= "<parameter=" "limit" ">\n" number "</parameter>\n"?
tool-process-arg-literal ::= "<parameter=" "literal" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-process-arg-offset ::= "<parameter=" "offset" ">\n" number "</parameter>\n"?
tool-process-arg-sessionId ::= "<parameter=" "sessionId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-process-arg-text ::= "<parameter=" "text" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-process-arg-timeout ::= "<parameter=" "timeout" ">\n" number "</parameter>\n"?
tool-read ::= "<function=" "read" ">\n" tool-read-arg-path? tool-read-arg-offset? tool-read-arg-limit? tool-read-arg-file-path? "</function>\n"
tool-read-arg-file-path ::= "<parameter=" "file_path" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-read-arg-limit ::= "<parameter=" "limit" ">\n" number "</parameter>\n"?
tool-read-arg-offset ::= "<parameter=" "offset" ">\n" number "</parameter>\n"?
tool-read-arg-path ::= "<parameter=" "path" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-session-status ::= "<function=" "session_status" ">\n" tool-session-status-arg-sessionKey? tool-session-status-arg-model? "</function>\n"
tool-session-status-arg-model ::= "<parameter=" "model" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-session-status-arg-sessionKey ::= "<parameter=" "sessionKey" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-history ::= "<function=" "sessions_history" ">\n" tool-sessions-history-arg-sessionKey tool-sessions-history-arg-limit? tool-sessions-history-arg-includeTools? "</function>\n"
tool-sessions-history-arg-includeTools ::= "<parameter=" "includeTools" ">\n" boolean "</parameter>\n"?
tool-sessions-history-arg-limit ::= "<parameter=" "limit" ">\n" number "</parameter>\n"?
tool-sessions-history-arg-sessionKey ::= "<parameter=" "sessionKey" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-list ::= "<function=" "sessions_list" ">\n" tool-sessions-list-arg-kinds? tool-sessions-list-arg-limit? tool-sessions-list-arg-activeMinutes? tool-sessions-list-arg-messageLimit? "</function>\n"
tool-sessions-list-arg-activeMinutes ::= "<parameter=" "activeMinutes" ">\n" number "</parameter>\n"?
tool-sessions-list-arg-kinds ::= "<parameter=" "kinds" ">\n" tool-sessions-list-arg-kinds-schema "</parameter>\n"?
tool-sessions-list-arg-kinds-schema ::= "[" space (string ("," space string)*)? "]" space
tool-sessions-list-arg-limit ::= "<parameter=" "limit" ">\n" number "</parameter>\n"?
tool-sessions-list-arg-messageLimit ::= "<parameter=" "messageLimit" ">\n" number "</parameter>\n"?
tool-sessions-send ::= "<function=" "sessions_send" ">\n" tool-sessions-send-arg-sessionKey? tool-sessions-send-arg-label? tool-sessions-send-arg-agentId? tool-sessions-send-arg-message tool-sessions-send-arg-timeoutSeconds? "</function>\n"
tool-sessions-send-arg-agentId ::= "<parameter=" "agentId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-send-arg-label ::= "<parameter=" "label" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-send-arg-message ::= "<parameter=" "message" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-send-arg-sessionKey ::= "<parameter=" "sessionKey" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-send-arg-timeoutSeconds ::= "<parameter=" "timeoutSeconds" ">\n" number "</parameter>\n"?
tool-sessions-spawn ::= "<function=" "sessions_spawn" ">\n" tool-sessions-spawn-arg-task tool-sessions-spawn-arg-label? tool-sessions-spawn-arg-runtime? tool-sessions-spawn-arg-agentId? tool-sessions-spawn-arg-model? tool-sessions-spawn-arg-thinking? tool-sessions-spawn-arg-cwd? tool-sessions-spawn-arg-runTimeoutSeconds? tool-sessions-spawn-arg-timeoutSeconds? tool-sessions-spawn-arg-thread? tool-sessions-spawn-arg-mode? tool-sessions-spawn-arg-cleanup? tool-sessions-spawn-arg-sandbox? tool-sessions-spawn-arg-attachments? tool-sessions-spawn-arg-attachAs? "</function>\n"
tool-sessions-spawn-arg-agentId ::= "<parameter=" "agentId" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-spawn-arg-attachAs ::= "<parameter=" "attachAs" ">\n" tool-sessions-spawn-arg-attachAs-schema "</parameter>\n"?
tool-sessions-spawn-arg-attachAs-schema ::= "{" space  (tool-sessions-spawn-arg-attachAs-schema-mountPath-kv )? "}" space
tool-sessions-spawn-arg-attachAs-schema-mountPath-kv ::= "\"mountPath\"" space ":" space string
tool-sessions-spawn-arg-attachments ::= "<parameter=" "attachments" ">\n" tool-sessions-spawn-arg-attachments-schema "</parameter>\n"?
tool-sessions-spawn-arg-attachments-schema ::= "[" space (tool-sessions-spawn-arg-attachments-schema-item ("," space tool-sessions-spawn-arg-attachments-schema-item){0,49})? "]" space
tool-sessions-spawn-arg-attachments-schema-item ::= "{" space tool-sessions-spawn-arg-attachments-schema-item-name-kv "," space tool-sessions-spawn-arg-attachments-schema-item-content-kv ( "," space ( tool-sessions-spawn-arg-attachments-schema-item-encoding-kv tool-sessions-spawn-arg-attachments-schema-item-encoding-rest | tool-sessions-spawn-arg-attachments-schema-item-mimeType-kv ) )? "}" space
tool-sessions-spawn-arg-attachments-schema-item-content ::= "\"" char{0,6700000} "\"" space
tool-sessions-spawn-arg-attachments-schema-item-content-kv ::= "\"content\"" space ":" space tool-sessions-spawn-arg-attachments-schema-item-content
tool-sessions-spawn-arg-attachments-schema-item-encoding ::= ("\"utf8\"" | "\"base64\"") space
tool-sessions-spawn-arg-attachments-schema-item-encoding-kv ::= "\"encoding\"" space ":" space tool-sessions-spawn-arg-attachments-schema-item-encoding
tool-sessions-spawn-arg-attachments-schema-item-encoding-rest ::= ( "," space tool-sessions-spawn-arg-attachments-schema-item-mimeType-kv )?
tool-sessions-spawn-arg-attachments-schema-item-mimeType-kv ::= "\"mimeType\"" space ":" space string
tool-sessions-spawn-arg-attachments-schema-item-name-kv ::= "\"name\"" space ":" space string
tool-sessions-spawn-arg-cleanup ::= "<parameter=" "cleanup" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-spawn-arg-cwd ::= "<parameter=" "cwd" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-spawn-arg-label ::= "<parameter=" "label" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-spawn-arg-mode ::= "<parameter=" "mode" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-spawn-arg-model ::= "<parameter=" "model" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-spawn-arg-runTimeoutSeconds ::= "<parameter=" "runTimeoutSeconds" ">\n" number "</parameter>\n"?
tool-sessions-spawn-arg-runtime ::= "<parameter=" "runtime" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-spawn-arg-sandbox ::= "<parameter=" "sandbox" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-spawn-arg-task ::= "<parameter=" "task" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-spawn-arg-thinking ::= "<parameter=" "thinking" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-sessions-spawn-arg-thread ::= "<parameter=" "thread" ">\n" boolean "</parameter>\n"?
tool-sessions-spawn-arg-timeoutSeconds ::= "<parameter=" "timeoutSeconds" ">\n" number "</parameter>\n"?
tool-subagents ::= "<function=" "subagents" ">\n" tool-subagents-arg-action? tool-subagents-arg-target? tool-subagents-arg-message? tool-subagents-arg-recentMinutes? "</function>\n"
tool-subagents-arg-action ::= "<parameter=" "action" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-subagents-arg-message ::= "<parameter=" "message" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-subagents-arg-recentMinutes ::= "<parameter=" "recentMinutes" ">\n" number "</parameter>\n"?
tool-subagents-arg-target ::= "<parameter=" "target" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-web-fetch ::= "<function=" "web_fetch" ">\n" tool-web-fetch-arg-url tool-web-fetch-arg-extractMode? tool-web-fetch-arg-maxChars? "</function>\n"
tool-web-fetch-arg-extractMode ::= "<parameter=" "extractMode" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-web-fetch-arg-maxChars ::= "<parameter=" "maxChars" ">\n" number "</parameter>\n"?
tool-web-fetch-arg-url ::= "<parameter=" "url" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-web-search-searxng ::= "<function=" "web_search_searxng" ">\n" tool-web-search-searxng-arg-query? tool-web-search-searxng-arg-count? "</function>\n"
tool-web-search-searxng-arg-count ::= "<parameter=" "count" ">\n" tool-web-search-searxng-arg-count-schema "</parameter>\n"?
tool-web-search-searxng-arg-count-schema ::= ([1-9] | "10") space
tool-web-search-searxng-arg-query ::= "<parameter=" "query" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-write ::= "<function=" "write" ">\n" tool-write-arg-path? tool-write-arg-content tool-write-arg-file-path? "</function>\n"
tool-write-arg-content ::= "<parameter=" "content" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-write-arg-file-path ::= "<parameter=" "file_path" ">\n" xml-arg-string "\n" "</parameter>\n"?
tool-write-arg-path ::= "<parameter=" "path" ">\n" xml-arg-string "\n" "</parameter>\n"?
value ::= object | array | string | number | boolean | null
xml-arg-string ::= ([^\n] | "\n" [^<] | "\n<" [^/p] | "\n</" [^fp] | "\n</f" [^u] | "\n</fu" [^n] | "\n</fun" [^c] | "\n</func" [^t] | "\n</funct" [^i] | "\n</functi" [^o] | "\n</functio" [^n] | "\n</function" [^>] | "\n</p" [^a] | "\n</pa" [^r] | "\n</par" [^a] | "\n</para" [^m] | "\n</param" [^e] | "\n</parame" [^t] | "\n</paramet" [^e] | "\n</paramete" [^r] | "\n</parameter" [^>] | "\n<p" [^a] | "\n<pa" [^r] | "\n<par" [^a] | "\n<para" [^m] | "\n<param" [^e] | "\n<parame" [^t] | "\n<paramet" [^e] | "\n<paramete" [^r] | "\n<parameter" [^=])*

llama_grammar_init_impl: failed to parse grammar
```

### Steps to reproduce

1. start llama-server llama-server.exe -m s:\.ollama\qwen35\Qwen3.5-35B-A3B-UD-Q4_K_M.gguf --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.00 --presence-penalty 0.0 --repeat-penalty 1.0 -c 99054 --fit on -fa on -t 8 --no-mmap --jinja -ctk q8_0 -ctv q8_0 --no-mmproj --swa-full --host 0.0.0.0 --sleep-idle-seconds 600

### Expected behavior

No errors with tools.

### Actual behavior

Errors with tools. (not sure but looks like something wrong with grammar in 2026.3.2)

### OpenClaw version

2026.3.2

### Operating system

ubuntu 24.04

### Install method

npm global

### Logs, screenshots, and evidence

```shell

```

### Impact and severity

_No response_

### Additional information

_No response_



I'll set an agent on figuring out why it could be.
```

## What you have

- `/testbed/repo` is a git clone of `openclaw/openclaw` truncated just after the regression was
  reported.  `HEAD` is `4ffe15c6b2227254e48b7724053d3c5079c9be6f` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.
