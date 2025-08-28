package site.ycsb.db.thesis;

import site.ycsb.*;

import java.util.*;
import java.io.IOException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;

import org.json.simple.JSONObject;


/**
 * Binding for the Thesis database.
 *
 */
public class ThesisClient extends DB {

    private HttpClient httpClient;
    private String baseUrl;
    private String getMethod;

    @Override
    public void init() throws DBException {
        System.out.println("Initializing ThesisClient...");

        baseUrl = getProperties().getProperty("thesis.ip", "http://localhost:8080");
        getMethod = getProperties().getProperty("thesis.get", "comm_ch"); // Options: "http" or "comm_ch"

        httpClient = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_2)
                .connectTimeout(java.time.Duration.ofSeconds(5))
                .build();
        
        // TODO: Find out why this is not working
        /*try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(baseUrl + "/api/test"))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString("{}"))
                    .build();
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() >= 300) {
                throw new DBException("Failed to connect to Thesis server at " + baseUrl + ". Status code: " + response.statusCode());
            }
        } catch (Exception e) {
            throw new DBException("Failed to connect to Thesis server at " + baseUrl);
        }
        System.out.println("ThesisClient initialized successfully with base URL: " + baseUrl);*/
    }

    @Override
    public void cleanup() throws DBException {
        System.out.println("Cleaning up ThesisClient...");
    }

    private void request(String endpoint, String json){
        try {

            //System.out.println("Making request to: " + baseUrl + endpoint);
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(baseUrl + endpoint))
                    .header("Content-Type", "application/json")
                    .header("Accept", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(json))
                    .build();
            
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            //Getting the response code
            int responsecode = response.statusCode();

            if(responsecode > 299) {
                System.out.println("Error: " + response.body());
                return;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public Status read(String table, String key, Set<String> fields, Map<String, ByteIterator> result) {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("partition", table);
        jsonObject.put("key", key);

        if(getMethod.equals("http"))
            request("/api/get", jsonObject.toString());
        else
            request("/api/get_comm_ch", jsonObject.toString());


        return Status.OK;
    }

    @Override
    public Status update(String table, String key, Map<String, ByteIterator> values) {
        insert(table, key, values);
        return Status.OK;
    }

    @Override
    public Status insert(String table, String key, Map<String, ByteIterator> values) {
        JSONObject jsonObject = new JSONObject();
        try{
            jsonObject.put("partition", table);
            jsonObject.put("key", key);
            jsonObject.put("value", serializeValues(values));
        } catch (IOException e) {
            e.printStackTrace();
        }
        request("/api/insert", jsonObject.toString());

        return Status.OK;
    }

    @Override
    public Status delete(String table, String key) {
        System.out.println("Deleting from ThesisClient: " + table + ", " + key);
        
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("partition", table);
        jsonObject.put("key", key);

        request("/api/remove", jsonObject.toString());

        return Status.OK;
    }

    @Override
    public Status scan(String table, String startkey, int recordcount, Set<String> fields, Vector<HashMap<String, ByteIterator>> result) {
        System.out.println("Scanning is not implemented in the Database!");
        return Status.Error;
    }

    @SuppressWarnings("unchecked")
    private String serializeValues(Map<String, ByteIterator> values) throws IOException {
        JSONObject jsonObject = new JSONObject();
        for (Map.Entry<String, ByteIterator> entry : values.entrySet()) {
            jsonObject.put(entry.getKey(), entry.getValue().toString());
        }
        return jsonObject.toString();
    }
}