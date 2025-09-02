const DEFAULT_PATTERNS: Array<[RegExp, string]> = [
  [/sk-[A-Za-z0-9]{20,}/g, 'sk-***REDACTED***'], // OpenAI-like keys
  [/api_key=([A-Za-z0-9-_]{10,})/gi, 'api_key=***REDACTED***'],
  [/(Authorization:\s*Bearer\s+)[A-Za-z0-9-_\.]+/gi, '$1***REDACTED***'],
  [/(OPENAI_API_KEY|ANTHROPIC_API_KEY|AZURE_OPENAI_KEY)=[^\s]+/g, '$1=***REDACTED***'],
]

export function redactString(input: string, extra?: Array<[RegExp, string]>): string {
  const patterns = [...DEFAULT_PATTERNS, ...(extra ?? [])]
  let out = input
  for (const [re, repl] of patterns) out = out.replace(re, repl)
  return out
}

export function redactObject<T extends Record<string, any>>(obj: T, keys: string[] = ['apiKey', 'password', 'token', 'authorization']): T {
  const clone: any = Array.isArray(obj) ? [...(obj as any)] : { ...obj }
  for (const k of Object.keys(clone)) {
    if (keys.includes(k)) {
      clone[k] = '***REDACTED***'
    } else if (clone[k] && typeof clone[k] === 'object') {
      clone[k] = redactObject(clone[k], keys)
    } else if (typeof clone[k] === 'string') {
      clone[k] = redactString(clone[k])
    }
  }
  return clone as T
}

export function safeErrorPayload(err: unknown): { name: string; code?: string; message: string } {
  const name = (err as any)?.name ?? 'Error'
  const message = typeof (err as any)?.message === 'string' ? redactString((err as any).message) : 'Error'
  const code = (err as any)?.code
  return { name, code, message }
}
