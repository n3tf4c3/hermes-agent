import assert from 'node:assert/strict'
import os from 'node:os'

import { beforeEach, test, vi } from 'vitest'

import { reviewRevert } from './git-review-ops'

// A partial failure (restore applied, clean refused) is not portable to provoke
// with a real repo, so drive reviewRevert against a git whose commands fail on
// demand. The real-repo cases live in git-review-ops.test.ts.
const calls: string[] = []
const failing = new Set<string>()

vi.mock('simple-git', () => {
  const git = {
    env: () => git,
    raw: async (args: string[]) => {
      calls.push(args[0])

      if (failing.has(args[0])) {
        throw new Error(`fatal: ${args[0]} refused`)
      }

      return args[0] === 'diff' ? 'tracked.txt\n' : ''
    }
  }

  return { simpleGit: () => git }
})

beforeEach(() => {
  calls.length = 0
  failing.clear()
})

test('reviewRevert reports a partial discard when clean fails after restore', async () => {
  failing.add('clean')

  await assert.rejects(
    reviewRevert(os.tmpdir(), null, 'git'),
    /tracked changes were discarded, but untracked files were not removed: fatal: clean refused/
  )
  assert.deepEqual(calls, ['diff', 'restore', 'clean'])
})

test('reviewRevert stops before clean when restore fails', async () => {
  failing.add('restore')

  await assert.rejects(
    reviewRevert(os.tmpdir(), 'tracked.txt', 'git'),
    /no changes were discarded: fatal: restore refused/
  )
  assert.deepEqual(calls, ['diff', 'restore'])
})

test('reviewRevert changes nothing when it cannot compare against HEAD', async () => {
  failing.add('diff')

  await assert.rejects(reviewRevert(os.tmpdir(), null, 'git'), /before changing anything: fatal: diff refused/)
  assert.deepEqual(calls, ['diff'])
})
