
import { NextApiRequest, NextApiResponse } from 'next'
import { generate_response } from '../../utils/chat_model'

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { prompt } = req.body
    if (!prompt) {
      return res.status(400).json({ error: 'Prompt is required' })
    }

    try {
      const response = await generate_response(prompt)
      return res.status(200).json({ response })
    } catch (error) {
      console.error('Error generating response:', error)
      return res.status(500).json({ error: 'Error generating response' })
    }
  } else {
    res.setHeader('Allow', ['POST'])
    res.status(405).end(`Method ${req.method} Not Allowed`)
  }
}
