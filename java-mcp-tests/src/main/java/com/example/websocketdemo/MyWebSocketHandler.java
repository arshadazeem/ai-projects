package com.example.websocketdemo;

import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;
import org.springframework.web.socket.TextMessage;

import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;

public class MyWebSocketHandler extends TextWebSocketHandler {

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        String payload = message.getPayload();
        System.out.println("Received: " + payload);
        session.sendMessage(new TextMessage("Echo: " + payload));
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        super.afterConnectionEstablished(session);
        Timer timer = new Timer();
        Random random = new Random();

        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                try {
                    String randomMessage = "Random automated msg from WS Server: " + generateRandomText();
                    session.sendMessage(new TextMessage(randomMessage));
                } catch (Exception e) {
                    e.printStackTrace();
                    timer.cancel();
                }
            }
        }, 0, (3) * 1000);
    }

    private String generateRandomText() {
        String[] messages = {"Hello!", "How are you?", "This is a random message.", "WebSocket is fun!", "Keep coding!"};
        return messages[new Random().nextInt(messages.length)];
    }
}
