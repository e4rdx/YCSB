package site.ycsb.db.thesis;

import site.ycsb.*;

import java.util.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import org.json.simple.JSONObject;


/**
 * Binding for the Thesis database.
 *
 */
public class ThesisClient extends DB {

    //final static 

    @Override
    public void init() throws DBException {
        System.out.println("Initializing ThesisClient...");
    }

    @Override
    public void cleanup() throws DBException {
        System.out.println("Cleaning up ThesisClient...");
    }

    private void request(String endpoint, String json){
        try {
            URL url = new URL(endpoint);

            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setDoOutput(true);
            conn.setRequestMethod("POST");
            conn.setReadTimeout(1000);
            
            // set headers
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setRequestProperty("Accept", "application/json");

            // set body
            System.out.println("JSON Input String: " + json);
            try(OutputStream os = conn.getOutputStream()) {
                byte[] input = json.getBytes("utf-8");
                os.write(input, 0, input.length);			
            }

            //Getting the response code
            int responsecode = conn.getResponseCode();

            System.out.println("Response Code: " + responsecode);

            System.out.println("Response Message: " + conn.getResponseMessage());

            if(responsecode > 299) {
                System.out.println("Error: " + conn.getResponseMessage());
                return;
            }

            try(BufferedReader br = new BufferedReader(
            new InputStreamReader(conn.getInputStream(), "utf-8"))) {
                StringBuilder response = new StringBuilder();
                String responseLine = null;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                System.out.println(response.toString());
            } catch(Exception e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public Status read(String table, String key, Set<String> fields, Map<String, ByteIterator> result) {
        System.out.println("Reading from ThesisClient: " + table + ", " + key);
        // Simulate a read operation
        result.put("field1", new ByteArrayByteIterator("value1".getBytes()));

        JSONObject jsonObject = new JSONObject();
        jsonObject.put("partition", table);
        jsonObject.put("key", key);

        request("http://192.168.0.161:8080/api/get", jsonObject.toString());


        return Status.OK;
    }

    @Override
    public Status update(String table, String key, Map<String, ByteIterator> values) {
        insert(table, key, values);
        System.out.println("Updating in ThesisClient: " + table + ", " + key);
        return Status.OK;
    }

    @Override
    public Status insert(String table, String key, Map<String, ByteIterator> values) {
        System.out.println("Inserting into ThesisClient: " + table + ", " + key);
  
        
        //String jsonInputString = "{\"key\":\"" + key + "\", \"value\":\"test\"}";
        JSONObject jsonObject = new JSONObject();
        try{
            jsonObject.put("partition", table);
            jsonObject.put("key", key);
            jsonObject.put("value", serializeValues(values));
        } catch (IOException e) {
            e.printStackTrace();
        }
        request("http://192.168.0.161:8080/api/insert", jsonObject.toString());

        return Status.OK;
    }

    @Override
    public Status delete(String table, String key) {
        System.out.println("Deleting from ThesisClient: " + table + ", " + key);
        
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("partition", table);
        jsonObject.put("key", key);

        request("http://192.168.0.161:8080/api/remove", jsonObject.toString());

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