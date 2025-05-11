package com.example.websocketdemo;

import org.junit.jupiter.api.Test;
import org.springframework.web.socket.client.standard.StandardWebSocketClient;
import org.springframework.web.socket.handler.AbstractWebSocketHandler;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class WebSocketTestClient {

    @Test
    public void testWebSocketEcho() throws Exception {
        StandardWebSocketClient client = new StandardWebSocketClient();
        CompletableFuture<String> future = new CompletableFuture<>();

        client.doHandshake(new AbstractWebSocketHandler() {
            @Override
            protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
                future.complete(message.getPayload());
            }
        }, "ws://localhost:8080/ws");

        WebSocketSession session = client.doHandshake(new AbstractWebSocketHandler() {
            @Override
            public void afterConnectionEstablished(WebSocketSession session) throws Exception {
                session.sendMessage(new TextMessage("Hello WebSocket"));
            }
        }, "ws://localhost:8080/ws").get();

        String response = future.get(5, TimeUnit.SECONDS);
        assertEquals("Echo: Hello WebSocket", response);

        session.close();
    }
}
