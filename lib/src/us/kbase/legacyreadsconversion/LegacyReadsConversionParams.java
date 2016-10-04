
package us.kbase.legacyreadsconversion;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: legacyReadsConversionParams</p>
 * <pre>
 * This module has methods to convert legacy KBaseAssembly types to 
 *                 KBaseFile types.
 *                 1. KBaseAssembly.SingleEndLibrary to KBaseFile.SingleEndLibrary
 *                 2. KBaseAssembly.PairedEndLibrary to KBaseFile.PairedEndLibrary
 *                 workspace_name    - the name of the workspace for input/output
 *                 read_library_name - the name of the KBaseAssembly.SingleEndLibrary or 
 *                         KBaseAssembly.PairedEndLibrary
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "read_library_name"
})
public class LegacyReadsConversionParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("read_library_name")
    private String readLibraryName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public LegacyReadsConversionParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("read_library_name")
    public String getReadLibraryName() {
        return readLibraryName;
    }

    @JsonProperty("read_library_name")
    public void setReadLibraryName(String readLibraryName) {
        this.readLibraryName = readLibraryName;
    }

    public LegacyReadsConversionParams withReadLibraryName(String readLibraryName) {
        this.readLibraryName = readLibraryName;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((("LegacyReadsConversionParams"+" [workspaceName=")+ workspaceName)+", readLibraryName=")+ readLibraryName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
