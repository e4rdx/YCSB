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

    @Override
    public void init() throws DBException {
        System.out.println("Initializing ThesisClient...");

        baseUrl = getProperties().getProperty("thesis.ip", "http://localhost:8080");

        httpClient = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_2)
                .connectTimeout(java.time.Duration.ofSeconds(5))
                .build();
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
        //System.out.println("Reading from ThesisClient: " + table + ", " + key);
        
        //result.put("field1", new ByteArrayByteIterator("value1".getBytes()));

        JSONObject jsonObject = new JSONObject();
        jsonObject.put("partition", table);
        jsonObject.put("key", key);

        request("/api/get", jsonObject.toString());


        return Status.OK;
    }

    @Override
    public Status update(String table, String key, Map<String, ByteIterator> values) {
        insert(table, key, values);
        //System.out.println("Updating in ThesisClient: " + table + ", " + key);
        return Status.OK;
    }

    @Override
    public Status insert(String table, String key, Map<String, ByteIterator> values) {
        //System.out.println("Inserting into ThesisClient: " + table + ", " + key);
  
        
        //String jsonInputString = "{\"key\":\"" + key + "\", \"value\":\"test\"}";
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
        System.out.println("Scanning in ThesisClient: " + table + ", starting from " + startkey + ", count: " + recordcount);
        // Simulate a scan operation
        return Status.OK;
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