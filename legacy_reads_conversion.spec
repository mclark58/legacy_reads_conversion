/*
Utilities for converting KBaseAssembly types to KBaseFile types
*/

module legacy_reads_conversion {
	/*

		This module has methods to convert legacy KBaseAssembly types to 
		KBaseFile types.
		1. KBaseAssembly.SingleEndLibrary to KBaseFile.SingleEndLibrary
		2. KBaseAssembly.PairedEndLibrary to KBaseFile.PairedEndLibrary

		workspace_name    - the name of the workspace for input/output
		read_library_name - the name of the KBaseAssembly.SingleEndLibrary or 
                        KBaseAssembly.PairedEndLibrary
		output            - the name of the output KBaseFiles.SingleEndLibrary or 
                        KBaseFiles.PairedEndLibrary
    sequencing_tech   - Sequencing technology used eg. Illumina
    single_genome     - Is it a single genome or metagenome?

	*/



	typedef structure {
		string workspace_name;
		string read_library_name;
		string sequencing_tech;
		int single_genome;
    string output;
	} legacyReadsConversionParams;



	typedef structure {
		string report_name;
		string report_ref;
	} ConversionReport;



funcdef run_legacy_reads_conversion (legacyReadsConversionParams input_params)
        returns (ConversionReport report)
        authentication required; 
 
};
